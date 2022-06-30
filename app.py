from distutils.log import info
import datadesc
from src.utils.Extractor import get_dataset_structure, extract_data_paper, extract_data_profile, extract_huggingFaceDataInfo, extract_schema_org, extract_readme_github
from sources.questions.Questions import get_questions
from src.schemaOrgMap import SchemaOrgMap
from src.dataProfileMap import DataProfileMap
from src.semantincSearch import SemanticSearch
from src.haystackQA import HaystackQA
import json
from collections import defaultdict


if __name__ == '__main__': 
    # ----------------------------------------------------------------
    # Variables to fill by the user
    # ----------------------------------------------------------------
    datasetWebsiteURL= 'https://www.kaggle.com/datasets/debarshichanda/goemotions'
    ReadmeSource = 'sources/datasets/goEmotions/readmeGithub.md'
    dataFolder = 'sources/datasets/goEmotions/data'
    paperPath = 'sources/datasets/goEmotions/goEmotionsPaper.pdf.tei.xml' ## Used GORBID to convert PDF to TEI.XML
    datasetName = 'goemotions'

    # Select the model to be used by the NLP extractors 
    # Need to be a name of https://www.sbert.net/docs/pretrained_models.html#
    modelName = 'cross-encoder/ms-marco-TinyBERT-L-2'

    # ----------------------------------------------------------------
    # Information parsers and extractors
    # ----------------------------------------------------------------
    metadataSchemaOrg = extract_schema_org(datasetWebsiteURL)
    ReadmeText = extract_readme_github(ReadmeSource)
    dataProfile = extract_data_profile(dataFolder)
    PaperText = extract_data_paper(paperPath)
    ## If its a HuggingFace dataset
    #datasetHuggingInfo = extract_huggingFaceDataInfo(datasetName)

    # ----------------------------------------------------------------
    # Auxiliar variables
    # ----------------------------------------------------------------
    datasetDescription = {
        'dataset' : get_dataset_structure(),
        'ToProcessWithNLP' : defaultdict(dict)
    }

    # ----------------------------------------------------------------
    # Mapping into the DSL from Schema.org
    # ----------------------------------------------------------------
    datasetDescription = SchemaOrgMap.map(metadataSchemaOrg,datasetDescription)

    # ----------------------------------------------------------------
    # Mapping into the DSL from data Profiling
    # ----------------------------------------------------------------
    datasetDescription = DataProfileMap.map(dataProfile, datasetDescription)

    # ----------------------------------------------------------------
    # Mapping into the DSL from data.json (HuggingFace)
    # ----------------------------------------------------------------
    ## TO DO


    # ----------------------------------------------------------------
    # Processing the extracted natural text
    # ----------------------------------------------------------------

    ## Formatting the text corpus
    corpusText = {
        'paper' : PaperText,
        'readme' : ReadmeText,
        'metadata' : datasetDescription['ToProcessWithNLP']
    } 

    ## TO DO: Develop an unified way to format the data for the different NLP stacks

    ## Get the proposed generic questions
    queries = get_questions(datasetDescription['dataset'])

    ## ----------------------------------------------------------------
    ## Using Sentence-Transformers for Semantinc Search using Retrival and ReRank
    ##
    ## More info: https://www.sbert.net/examples/applications/retrieve_rerank/README.html
    ## Example script: https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/retrieve_rerank/in_document_search_crossencoder.py
    ## --------------------------------------------------------------
    EmbeddingsBertOutput = SemanticSearch().search(corpusText,queries,modelName)

    ## ----------------------------------------------------------------
    ## Using Haystack with Retrival and Readers node 
    ##
    ## More info: https://haystack.deepset.ai/pipeline_nodes/retriever
    ## Example script: https://colab.research.google.com/github/deepset-ai/haystack/blob/master/tutorials/Tutorial3_Basic_QA_Pipeline_without_Elasticsearch.ipynb
    ## --------------------------------------------------------------
    #HaystackOutput = HaystackQA().search(corpusText,queries,modelName)


    # ----------------------------------------------------------------
    # Mapping answers into the DSL
    # TO DO
    ## Use the answers to refine questions
    ## TO DO
    # ----------------------------------------------------------------
     ## Prepare outfiles
    #meta = datasetDescription['dataset'].metadata

    #dest = datasetDescription['dataset'].__dict__
    datadescOut = open('out/datasetDescription.json', "w")
    print(json.dumps(datasetDescription, indent=2), file=datadescOut)
    datadescOut.flush()

    #Haoutfile = open('out/HaystackLog.json', "w")
    #print(json.dumps(HaystackOutput, indent=2), file=Haoutfile)
    #Haoutfile.flush()
   
    Emoutfile = open('out/EmbeddingsLog.json', "w")
    print(json.dumps(EmbeddingsBertOutput, indent=2), file=Emoutfile)
    Emoutfile.flush()

  

    print('ok')

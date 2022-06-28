from distutils.log import info
import datadesc
from src.utils.Extractor import extract_data_paper, extract_data_profile, extract_huggingFaceDataInfo, extract_schema_org, extract_readme_github
from sources.questions.Questions import get_questions
from src.schemaOrgMap import SchemaOrgMap
from src.dataProfileMap import DataProfileMap
from src.semantincSearch import SemanticSearch
import json


# ----------------------------------------------------------------
# Variables to fill by the user
# ----------------------------------------------------------------
datasetWebsiteURL= 'https://www.kaggle.com/datasets/debarshichanda/goemotions'
ReadmeSource = 'sources/datasets/goEmotions/readmeGithub.md'
dataFolder = 'sources/datasets/goEmotions/data'
paperPath = 'sources/datasets/goEmotions/goEmotionsPaper.pdf.tei.xml' ## Used GORBID to convert PDF to TEI.XML
datasetName = 'goemotions'

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
    'dataset' : datadesc.DatasetDescription(),
    'ToProcessWithNLP' : {}
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
# First attempt to NLP
# ----------------------------------------------------------------
## Get questions
queries = get_questions(datasetDescription['dataset'])
## Formatting text corpus
naturalText = {
    'paper' : PaperText,
    'readme' : ReadmeText,
    'metadata' : datasetDescription['ToProcessWithNLP']
} 
## Using embedding directly 
datasetDescription = SemanticSearch().search(datasetDescription,naturalText,queries)

## Using Haystack



## NLP extractors 
## Create a set of questions to extract information from paper and readme Github
## Prepare data for the NLP models
## Compute the models
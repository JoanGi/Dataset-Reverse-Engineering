# Getting URL information
import extruct
from w3lib.html import get_base_url
import markdown2
from bs4 import BeautifulSoup
import pandas as pd
import glob
from pandas_profiling import ProfileReport
from utils.TEIparser import TEIFile
import json
from asyncio.windows_events import NULL
import os
from datasets import get_dataset_infos


def extract_huggingFaceDataInfo(datasetName):
    return get_dataset_infos(datasetName)

def extract_schema_org(url):
    ## 1 - EXTRACT FROM THE SEMANTIC OF URL (ONLY APPLIES WEBS CORRECTLY ANNOTATED WITH JOSN-LD SCHEMA.ORG)
    #res = requests.get(url)
    #html = res.text
    html = open('sources/metadataSchemaOrg.html', 'r').read()
    metadataSchemaOrg = extruct.extract(
            html,
            base_url=get_base_url(html, url),
            syntaxes=['json-ld'],
        )['json-ld'][0]
    return metadataSchemaOrg


def extract_readme_github(readmeFolder):
    ## 2 - Get ReadMe from repository
    mdReadme = open(readmeFolder, 'r').read()
    html = markdown2.markdown(mdReadme)
    htmlParse = BeautifulSoup(html, 'html.parser')
    print(htmlParse.get_text())
    readMeGitHub = htmlParse.findChildren(recursive=False)
    return readMeGitHub

def extract_data_profile(dataFolder):
    ## 3 - Get Information from the data
    ### Read the data from sources/data (in .csv) and write a data profile in /sources
    #dataFolder = 'sources/data'
    if (os.path.exists('sources/dataProfile.json')):
        print('Data Profile already exists in sources/dataProfile.json, delete it to calculate again')
        with open('sources/dataProfile.json', 'r') as outfile:
            return json.load(outfile)
    else:
        df = pd.concat(map(pd.read_csv, glob.glob(dataFolder + "/*.csv")))
        profile = ProfileReport(df, title="Pandas Profiling Report")
        json_profile = profile._render_json()
        with open('sources/dataProfile.json', 'w') as outfile:
            outfile.write(json_profile)
    return json_profile

def extract_data_paper(TEIsource):

    ## 4 - Get information from the paper
    ### Convert PDF to TEI
    ### Parse TEI into JSON NLP friendly data format
    tei = TEIFile(TEIsource)
    text = tei.text;

    ### Question to answer by the model
    questions = {
        "question": "",
        "question_id": "",
        "answers": [
            {
                "answer": {
                    "unanswerable": False,
                    "extractive_spans": [],
                    "yes_no": NULL,
                    "free_form_answer": "",
                    "evidence": [
                    ],
                    "highlighted_evidence": [
                    ]
                }
            }
        ]
    }
    sections = text['sections']
    ### Data well-formated for NLP models
    paper = {
        'test' : {
            'title':tei.title,
            'abstract': tei.abstract,
            'full_text': text['sections'],
            'qas': [questions]
        }
    }
    ### Save data well formatted in /sources
    outfile = open("sources/goEmotionsPaperForNLP.json", "w")
    print(json.dumps(paper, indent=4), file=outfile)
    return paper
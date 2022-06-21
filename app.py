import datadesc
from utils.Extractor import extract_data_paper, extract_data_profile, extract_schema_org, extract_readme_github

## Variables to fill by the user
datasetWebsiteURL= 'https://www.kaggle.com/datasets/debarshichanda/goemotions'
ReadmeSource = 'sources/readmeGithub.md'
dataFolder = 'sources/data'
paperPath = 'sources/goEmotionsPaper.pdf.tei.xml' ## Used GORBID to convert PDF to TEI.XML

## Information parsers and extractors
metadataSchemaOrg = extract_schema_org(datasetWebsiteURL)
ReadmeText = extract_readme_github(ReadmeSource)
dataProfile = extract_data_profile(dataFolder)
PaperText = extract_data_paper(paperPath)

## NLP extractors
### TO DO

## Mapping into the DSL
if (metadataSchemaOrg['@type'] == 'Dataset'):
    dataset = datadesc.DatasetDescription()
    ### Title
    dataset.metadata['Title'] = metadataSchemaOrg['name']
    ### Licenses
    dataset.metadata['Licenses'] = metadataSchemaOrg['license']
    #### Date Modified
    # TO FIX: dataset.metadata['Release Data'] = metadataSchemaOrg['distribution']['dateModified']
    for keywordRow in metadataSchemaOrg['keywords']:
        if (keywordRow[0] == 'subject'):
            for key in keywordRow:
    ### Areas
                dataset.metadata['Area'].append(key) # TODO allow multi tags in AREA
        if (keywordRow[0] == 'technique'):
            for key in keywordRow:
    ### Description - Tasks
                dataset.metadata['Description']['Tasks'].append(key) # TODO allow multi tags in AREA
    ### Authors ... and Much more...








from distutils.log import info
import datadesc
from utils.Extractor import extract_data_paper, extract_data_profile, extract_huggingFaceDataInfo, extract_schema_org, extract_readme_github
import json
import jsonpickle
# ----------------------------------------------------------------
# Variables to fill by the user
# ----------------------------------------------------------------
datasetWebsiteURL= 'https://www.kaggle.com/datasets/debarshichanda/goemotions'
ReadmeSource = 'sources/readmeGithub.md'
dataFolder = 'sources/data'
paperPath = 'sources/goEmotionsPaper.pdf.tei.xml' ## Used GORBID to convert PDF to TEI.XML
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
## Extracted information that need to be computed by an NLP Model later on 
InformationToProcessWithNLP = {}
## Dict representation of our dataset DSL 
dataset = datadesc.DatasetDescription()


# ----------------------------------------------------------------
# Mapping into the DSL from Schema.org
# ----------------------------------------------------------------
if (metadataSchemaOrg['@type'] == 'Dataset'):
   
    ### Title and identifier
    if 'name' in metadataSchemaOrg:
        dataset.metadata['Title'] = metadataSchemaOrg['name']
    if 'issn' in metadataSchemaOrg:
        dataset.metadata['UniqueIdentifier'] = metadataSchemaOrg['issn']
    else:  
        if 'identifier' in metadataSchemaOrg:
            dataset.metadata['UniqueIdentifier'] = metadataSchemaOrg['identifier']

    ### Versioning
    if 'version' in metadataSchemaOrg:
        dataset.metadata['Version'] = metadataSchemaOrg['version']

    ### Description
    if 'description' in metadataSchemaOrg:
        InformationToProcessWithNLP["description"] = metadataSchemaOrg['description']
    if 'inLanguage' in metadataSchemaOrg:
        InformationToProcessWithNLP["language"] = metadataSchemaOrg['inLanguage']
    
    ### Licenses and Distribution
    if 'license' in metadataSchemaOrg:
        dataset.metadata['Licenses'] = metadataSchemaOrg['license']
    if 'isAccessibleForFree' in metadataSchemaOrg:
        dataset.metadata['Distribution']['isPublic'] = metadataSchemaOrg['isAccessibleForFree'];
    if 'distribution' in metadataSchemaOrg:
        dataset.metadata['Distribution']['How is distributed'] = metadataSchemaOrg['distribution'];
    if 'copyrightNotice' in metadataSchemaOrg:
        dataset.metadata['Distirbution']['Distribution Licenses'] = metadataSchemaOrg['copyrightNotice']

    ### Usages
    if 'usageInfo' in metadataSchemaOrg:
        InformationToProcessWithNLP["uses"] = metadataSchemaOrg['usageInfo']

    #### Dates
    if 'dateCreated' in metadataSchemaOrg:
        dataset.metadata['Release Data'] = metadataSchemaOrg['dateCreated']    
    if 'dateModified' in metadataSchemaOrg:
        dataset.metadata['Update Data'] = metadataSchemaOrg['dateModified']
    if 'datePublished' in metadataSchemaOrg:
        dataset.metadata['Published Data'] = metadataSchemaOrg['datePublished']

    ## Citation
    if 'citation' in metadataSchemaOrg:
        dataset.metadata['Citation'] = metadataSchemaOrg['citation']

    ### Accesiblity
    if 'accessibilitySummary' in metadataSchemaOrg:
        dataset.socialConcerns["Social Issues"].append(
            {
            "Issue Name":'Accesiblity',
            "Description": metadataSchemaOrg['accessibilitySummary']
            }
        )


    ### Areas, Tags and Tasks
    if 'keywords' in metadataSchemaOrg:
        for keywordRow in metadataSchemaOrg['keywords']:
            keywordRow = keywordRow.split(',')
            if (keywordRow[0] == 'subject'):
                for key in keywordRow:
                    dataset.metadata['Area'].append(key) # TODO allow multi tags in AREA
            elif (keywordRow[0] == 'technique'):
                for key in keywordRow:
                    dataset.metadata['Description']['Tasks'].append(key)
            else:
                for key in keywordRow:
                    dataset.metadata['Tags'].append(key)


    ## Authors
    if 'author' in metadataSchemaOrg:
        for author in metadataSchemaOrg['author']:
            dataset.metadata['Authoring']['Authors'].append(author)
    elif 'creator' in metadataSchemaOrg:
        dataset.metadata['Authoring']['Authors'].append(metadataSchemaOrg['creator'])

    ### Funders
    if 'funders' in metadataSchemaOrg:
        dataset.metadata['Authoring']['Funders'].append(metadataSchemaOrg['funders'])
    if 'funding' in metadataSchemaOrg:
        dataset.metadata['Authoring']['Funders'].append(metadataSchemaOrg['funding'])
    
    ### Mantainers
    if 'maintainer' in metadataSchemaOrg:
        dataset.metadata['Authoring']['Mantainers'].append(metadataSchemaOrg['mantainer'])

    ### Spatial Reference
    ##if 'spatialCoverage' in metadataSchemaOrg:
        ## TODO
      ### Spatial Reference
    ##if 'temporalCoverage' in metadataSchemaOrg:
        ## TODO


# ----------------------------------------------------------------
# Mapping into the DSL from data Profiling
# ----------------------------------------------------------------

dataset.composition['Total Size'] = dataProfile['table']['n']
typesString = 'The features type are: '
for types in dataProfile['table']['types']:
    print(types)
    print(dataProfile['table']['types'][types])
    typesString = typesString+' '+ types+': '+str(dataProfile['table']['types'][types])

dataset.composition['Instances']['Instance Name'] = 'Instance1'
dataset.composition['Instances']['Type'] = 'Tabular Data'
dataset.composition['Instances']['Attribute Number'] = dataProfile['table']['n_var']
dataset.composition['Instances']['Size'] = dataProfile['table']['n']
for key, variables in dataProfile['variables'].items():

    if (variables['type'] == 'Categorical'):
        dataset.composition['Instances']['Attributes'].append({
            'Attribute name': key,
            'Count': variables['n'],
            'OfType': variables['type'],
            'Statistics': {
                ## Counts
                'Unique': variables['n_distinct'],
                'Unique percentage': variables['p_distinct'],
                'Missing Values': variables['n_missing'],
                'Completeness': 100 - variables['p_missing'],
                'First rows': variables['first_rows'],

                ## Lenghts
                'Min-length': variables['min_length'],
                'Max-length': variables['max_length'],
                'Median-length': variables['median_length'],
                'Length-histogram': variables['length_histogram'],


                ## Categorical Distribution
                'Categorical Distribution': variables['value_counts_index_sorted'],
                'Chi Squared': variables['chi_squared'],

                ## Category counts
                'Word Count': variables['word_counts'],
                'Category alias Counts': variables['category_alias_counts'],
                'Script char Counts': variables['script_char_counts'],
                'Block alias Counts': variables['block_alias_counts']   
            }
        })
    elif (variables['type'] == 'Numeric'):
        dataset.composition['Instances']['Attributes'].append({
                    'Attribute name': key,
                    'Count': variables['n'],
                    'OfType': variables['type'],
                    'Statistics': {}
        })
    elif (variables['type'] == 'Boolean'):
        dataset.composition['Instances']['Attributes'].append({
                    'Attribute name': key,
                    'Count': variables['n'],
                    'OfType': variables['type'],
                    'Statistics': {}
        })
dataset.composition['Instances']['Statistics'].append(
    {
        'Correlations': {
            'Pearson':dataProfile['correlations']['pearson'],
            'Spearman':dataProfile['correlations']['spearman'],
            'Kendall':dataProfile['correlations']['kendall'],
            'Cramers':dataProfile['correlations']['cramers'],
            'Phi_k':dataProfile['correlations']['phi_k'],
        }
    })


## DOES NOT WORK TO ENCONDE JSON
with open('out/datadesc.json', 'w') as outfile:
    outfile.write(jsonpickle.encode(dataset, unpicklable=False))

print(typesString)

## NLP extractors 

## Create a set of questions to extract information from paper and readme Github

## Prepare data for the NLP models

## Compute the models







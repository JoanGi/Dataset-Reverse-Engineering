from collections import defaultdict

class SchemaOrgMap:

    def map(metadataSchemaOrg, datasetDescription):

        # Auxiliar variables
        dataset = datasetDescription['dataset']
        ToProcessWithNLP = datasetDescription['ToProcessWithNLP']

        # ----------------------------------------------------------------
        # Mapping into the DSL from Schema.org
        # ----------------------------------------------------------------
        if (metadataSchemaOrg['@type'] == 'Dataset'):
        
            ### Title and identifier
            if 'name' in metadataSchemaOrg:
                dataset['metadata']['Title'] = metadataSchemaOrg['name']
            if 'issn' in metadataSchemaOrg:
                dataset['metadata']['Unique-Identifier'] = metadataSchemaOrg['issn']
            else:  
                if 'identifier' in metadataSchemaOrg:
                    dataset['metadata']['Unique-Identifier'] = metadataSchemaOrg['identifier']

            ### Versioning
            if 'version' in metadataSchemaOrg:
                dataset['metadata']['Version'] = metadataSchemaOrg['version']

            ### Description
            if 'description' in metadataSchemaOrg:
                ToProcessWithNLP["description"] = metadataSchemaOrg['description']
            if 'inLanguage' in metadataSchemaOrg:
                ToProcessWithNLP["language"] = metadataSchemaOrg['inLanguage']
            
            ### Licenses and Distribution
            if 'license' in metadataSchemaOrg:
                dataset['metadata']['Licenses'].append(metadataSchemaOrg['license'])

            if 'isAccessibleForFree' in metadataSchemaOrg:
                dataset['metadata']['Distribution']['isPublic'] = metadataSchemaOrg['isAccessibleForFree'];
            if 'distribution' in metadataSchemaOrg:
                dataset['metadata']['Distribution']['How is distributed'] = metadataSchemaOrg['distribution'];
            if 'copyrightNotice' in metadataSchemaOrg:
                dataset['metadata']['Distirbution']['Distribution Licenses'] = metadataSchemaOrg['copyrightNotice']

            ### Usages
            if 'usageInfo' in metadataSchemaOrg:
               ToProcessWithNLP["uses"] = metadataSchemaOrg['usageInfo']

            #### Dates
            if 'dateCreated' in metadataSchemaOrg:
                dataset['metadata']['Release Date'] = metadataSchemaOrg['dateCreated']    
            if 'dateModified' in metadataSchemaOrg:
                dataset['metadata']['Update Date'] = metadataSchemaOrg['dateModified']
            if 'datePublished' in metadataSchemaOrg:
                dataset['metadata']['Published Date'] = metadataSchemaOrg['datePublished']

            ## Citation
            if 'citation' in metadataSchemaOrg:
                dataset['metadata']['Citation'] = metadataSchemaOrg['citation']

            ### Accesiblity
            if 'accessibilitySummary' in metadataSchemaOrg:
                dataset['socialConcerns']["Social Issues"].append(
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
                            dataset['metadata']['Area'].append(key) # TODO allow multi tags in AREA
                    elif (keywordRow[0] == 'technique'):
                        for key in keywordRow:
                            dataset['metadata']['Description']['Tasks'].append(key)
                    else:
                        for key in keywordRow:
                            dataset['metadata']['Tags'].append(key)


            ## Authors
            if 'author' in metadataSchemaOrg:
                #dataset['metadata']['Authoring']['Authors'] = {}
                for author in metadataSchemaOrg['author']:
                    dataset['metadata']['Authoring']['Authors'].append(author)
            elif 'creator' in metadataSchemaOrg:
                dataset['metadata']['Authoring']['Authors'].append(metadataSchemaOrg['creator'])

            ### Funders
            if 'funders' in metadataSchemaOrg:
                dataset['metadata']['Authoring']['Funders'].append(metadataSchemaOrg['funders'])
            if 'funding' in metadataSchemaOrg:
                dataset['metadata']['Authoring']['Funders'].append(metadataSchemaOrg['funding'])
            
            ### Mantainers
            if 'maintainer' in metadataSchemaOrg:
                dataset['metadata']['Authoring']['Mantainers'].append(metadataSchemaOrg['mantainer'])

            ### Spatial Reference
            ##if 'spatialCoverage' in metadataSchemaOrg:
                ## TODO


            datasetDescription['dataset'] = dataset
            datasetDescription['ToProcessWithNLP'] = ToProcessWithNLP

            return datasetDescription




class DataProfileMap:

    def map(dataProfile, datasetDescription):
        ## Auxiliar Variables
        dataset = datasetDescription['dataset']

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

        datasetDescription['dataset'] = dataset
        return datasetDescription
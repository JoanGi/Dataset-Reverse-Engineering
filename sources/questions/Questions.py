
def get_questions(dataset):
    ## The questies to search in the document
    queries = [ 
                # Description
                "What is "+dataset['metadata']['Title']+" dataset?",
                "What is "+dataset['metadata']['Title']+" about?",
                "Which are the purposes "+dataset['metadata']['Title']+" fills?",
                "Which gaps "+dataset['metadata']['Title']+" fills?",
                "What demonstrate "+dataset['metadata']['Title']+" dataset?",
                "Which experiments has been conducted?",
                # Uses
                "Is there recommended uses for dataset?",
                "Is there non-recommended uses for "+dataset['metadata']['Title']+" dataset?",
                "Has the dataset been used before?",

                # Distribution
                "Is there any distribution policy for the dataset?",
                "How the dataset is distributed?",

                # Authoring
                "Who are the funders dataset?",
                "Who is the maintainer of the "+dataset['metadata']['Title']+" dataset?",
                "Is there any erratum?",
                "Which are the updating policies of "+dataset['metadata']['Title']+" dataset?",
                "Which are the contributing guidelines?",


                # Composition
                "Which are the composition of "+dataset['metadata']['Title']+" dataset?",
                "Which type of data "+dataset['metadata']['Title']+" is composed?",

                # Provenance
                "How has been "+dataset['metadata']['Title']+" data collected?",
                "How has been "+dataset['metadata']['Title']+" data gathered?",
                "How has been "+dataset['metadata']['Title']+" data labeled?",
                "How has been "+dataset['metadata']['Title']+" data selected?",
                "How was the process for selecting "+dataset['metadata']['Title']+" data?",
    
                # Social Concenrs
                "Is there any bias in "+dataset['metadata']['Title']+" dataset?",
                "Is there any privacy issues in "+dataset['metadata']['Title']+" dataset?",
                "Is there any social concern in "+dataset['metadata']['Title']+" dataset?"
                "Are there potential harmful data in "+dataset['metadata']['Title']+" dataset?"
                ]   

    for attribute in dataset['composition']['Instances']['Attributes']:
        if 'Attribute name' in attribute:
            queries.append("What is the attribute "+attribute['Attribute name']+" about?")
            queries.append("A description of the attribute "+attribute['Attribute name']+"?")
    return queries
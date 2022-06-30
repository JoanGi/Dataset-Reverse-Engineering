from haystack.pipelines import Pipeline
from haystack.nodes import Crawler, PreProcessor, FARMReader, TfidfRetriever, EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import MarkdownConverter 
from pathlib import Path
from haystack.utils.preprocessing import convert_files_to_docs

class HaystackQA:

    def search(self, textCorpus, questions, modelName):
        #
        # Step 1: Get the data, clean it, and store it.
        #

        # NOTE: If you a persistent document store, you can run this code only once

        # We initialize a document store (could be ElasticSearch and more see Haystack documentation)
        document_store = InMemoryDocumentStore(embedding_dim=384, similarity='cosine')

        # We initialize a preprocessor to convert the textCorpus in a frendly way to the Retriever
        preprocessor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=False,
            split_by="word",
            split_length=500,
            split_respect_sentence_boundary=True,
        )

        ## We convert the files in the folder to Haystack firendly documents
        docs = convert_files_to_docs(dir_path=Path('sources\datasets\goEmotions\\test'))
        
        ## We preprocess the files
        docs = preprocessor.process(docs)

        ## We store it in the document store
        document_store.write_documents(docs)

        #
        # Step 2: Configure the pipeline
        #

        # NOTE: You can run this code as many times as you like.

        # Let's create a query pipeline. It will contain:
        #  1. A Retriever that gets the relevant documents from the document store.
        #  2. A Reader that locates the answers inside the documents.

        
        #retriever = TfidfRetriever(document_store=document_store)
        retriever = EmbeddingRetriever(
            document_store=document_store,
        embedding_model="sentence-transformers/all-MiniLM-L12-v2",
        model_format="sentence_transformers",
        use_gpu=False,
        )
        document_store.update_embeddings(retriever)

        reader =  FARMReader(
            model_name_or_path="deepset/minilm-uncased-squad2", 
            use_gpu= False,
            context_window_size=350)

        query_pipeline = Pipeline()
        query_pipeline.add_node(component=retriever, name="retriever", inputs=["Query"])
        query_pipeline.add_node(component=reader, name="reader", inputs=["retriever"])


        #
        # Step 3: Run the pipeline for every question
        #
        output_data = []
        #for question in questions:  
        results = query_pipeline.run_batch(queries=questions, params={"retriever": {"top_k": 10}, "reader": {"top_k": 5}})
        output_data.append({'Query':results['query'],'Answers':results['answers']})
        
        print("\nQuestion: ", results["query"])
        print("\nAnswers:")
        for answer in results["answers"]:
            print("- ", answer.answer)
        print("\n\n")

        print('ok')
        return output_data



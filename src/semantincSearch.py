"""
This example show how in-document search can be used with a CrossEncoder.
The document is split into passage. Here, we use three consecutive sentences as a passage. You can use shorter passage, for example, individual sentences,
or longer passages, like full paragraphs.
The CrossEncoder takes the search query and scores every passage how relevant the passage is for the given score. The five passages with the highest score are  then returned.
As CrossEncoder, we use cross-encoder/ms-marco-TinyBERT-L-2, a BERT model with only 2 layers trained on the MS MARCO dataset. This is an extremely quick model able to score up to 9000 passages per second (on a V100 GPU). You can also use a larger model, which gives better results but is also slower.
Note: As we score the [query, passage]-pair for every new query, this search method
becomes at some point in-efficient if the document gets too large.
Usage: python in_document_search_crossencoder.py
"""

from asyncio import windows_events
from sentence_transformers import CrossEncoder
from nltk import sent_tokenize
import time
import json


class SemanticSearch:

       

    def search(self, naturalText, queries, modelName):

        paragraphs = []

        ##
        # Preprocess the Paper
        #
        # TO DO: ADD abstract, ADD title to paragraphs
        ##
        #### preProcessParagraphs.append('Abstract: '+paper['test']['abstract'])
        answer = self.get_passages(naturalText['paper']['test']['full_text'])
        paragraphs = answer['paragraphs']
        passages = answer['passages']
    
        Pasoutfile = open('sources/datasets/goEmotions/paper.json', "w")
        print(json.dumps(passages, indent=2), file=Pasoutfile)

        ##
        # Preprocess the readme
        ##
        readmeFormatted = [{'paragraphs' : naturalText['readme'].replace("\r\n", "\n").split("\n\n")}]
        answer = self.get_passages(readmeFormatted)
        ## A
        for paragraph in answer['paragraphs']:
            paragraphs.append(paragraph) 
        for passage in answer['passages']:
            passages.append(passage.replace("\n", " " ))


        ##
        # Preprocess the metadata get from schema and 
        ##
        for key, data in naturalText['metadata'].items():
            passages.append(key +': '+ data.replace("\n", " "))

        print("Paragraphs: ", len(paragraphs))
        print("Sentences: ", sum([len(p) for p in paragraphs]))
        print("Passages: ", len(passages))

        ## Save Text passages

        ## Prepare outfile
        outfile = open('out/log.json', "w")
        output = []
        ## Load our cross-encoder. Use fast tokenizer to speed up the tokenization
        model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2')
        start_time = time.time()

        #Search in a loop for the individual queries
        for query in queries:

            #Concatenate the query and all passages and predict the scores for the pairs [query, passage]
            model_inputs = [[query, passage] for passage in passages]
            scores = model.predict(model_inputs)

            #Sort the scores in decreasing order
            results = [{'input': inp, 'score': score} for inp, score in zip(model_inputs, scores)]
            results = sorted(results, key=lambda x: x['score'], reverse=True)
            output_data = {
                    "question": query,
                    "answers": []
            }
            print("Query:", query)
      
            for hit in results[0:5]:
                output_data['answers'].append(("Score: {:.2f}".format(hit['score']),  hit['input'][1]))
                print("Score: {:.2f}".format(hit['score']), "\t", hit['input'][1])

            output.append(output_data)
            print("==========")
        print("Search took {:.2f} seconds".format(time.time() - start_time))
    
        return output
        

    def get_passages(self,sections):
        paragraphs = []
        for section in sections: 
        ## We split this article into paragraphs and then every paragraph into sentences
            for paragraph in section['paragraphs']:
                if len(paragraph.strip()) > 0:
                    paragraphs.append(sent_tokenize(paragraph.strip()))

        #We combine up to 3 sentences into a passage. You can choose smaller or larger values for window_size
        #Smaller value: Context from other sentences might get lost
        #Lager values: More context from the paragraph remains, but results are longer
        passages = []
        window_size = 10
        for paragraph in paragraphs:
            for start_idx in range(0, len(paragraph), window_size):
                end_idx = min(start_idx+window_size, len(paragraph))
                passages.append(" ".join(paragraph[start_idx:end_idx]))
        answer = {
            'passages': passages,  
            'paragraphs': paragraphs
        }
        return answer
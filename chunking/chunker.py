from openai_client import *
from data_wrangler import *

class Chunker:

    def __init__(self) -> None:
        self.client = Gpt()
        self.db_manager = DataWrangler()

    def __summarize_pair(self, chunk1, chunk2):
        return self.client.summarize_pair(chunk1, chunk2)

    def insert_layers(self, pyramid):
        for layer, layer_chunks in enumerate(pyramid):
            for chunk in layer_chunks:
                embedding, shape = self.client.encode_text(chunk)
                self.db_manager.add_chunk(chunk, embedding, shape, layer)
                
    def create_summary_pyramid(self, chunks, max_layers=5):
        pyramid = [chunks]  # Bottom layer
        
        for layer in range(1, max_layers):
            new_layer = []
            for i in range(0, len(pyramid[-1]), 2):
                if i + 1 < len(pyramid[-1]):
                    combined = self.__summarize_pair(pyramid[-1][i], pyramid[-1][i+1])
                else:
                    combined = pyramid[-1][i]  # If odd number, keep last chunk as is
                new_layer.append(combined)
            
            pyramid.append(new_layer)
            
            if len(new_layer) == 1:
                break  # We've reached the top of the pyramid
        
        return pyramid

    def read_and_chunk_file(self, content, chunk_size=500, overlap=100):
        chunks = []
        start = 0

        #looping through file chunk at a time
        while start < len(content):
            end = start + chunk_size
            chunk = content[start:end]
              
            if end < len(content):
                #finds sentence end of chunk or paragraph end of chunk then moves end to that spot + 1 after new para or period
                sentence_end = chunk.rfind('.')
                paragraph_end = chunk.rfind('\n')
                if sentence_end > 0:
                    end = start + sentence_end + 1
                elif paragraph_end > 0:
                    end = start + paragraph_end + 1

                chunks.append(content[start:end])
        return chunks

    
   
import sqlite3
from openai_client import *

class DataWrangler:

    def __init__(self) -> None:
        conn = sqlite3.connect('../../premera_plan.sqlite')
        self._db_cursor = conn.cursor()
        self.client = Gpt()

    def initialize(self):
        self._db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_chunks
            (id INTEGER PRIMARY KEY, content TEXT, embedding BLOB, shape TEXT, layer INTEGER)
            ''')
        
    def __fetch_all(self):
        self._db_cursor.execute('SELECT id, embedding, shape, layer FROM document_chunks')
        return self._db_cursor.fetchall()

    def __find_similiarities(self, top_ids):
        placeholders = ','.join('?' for _ in top_ids)
        self._db_cursor.execute(f'SELECT content, layer FROM document_chunks WHERE id IN ({placeholders})', 
                    [id for id, _, _ in top_ids])
        return self._db_cursor.fetchall()

    def retrieve_chunks(self, query, top_k=5):
        query_embedding, query_shape = self.client.encode_text(query)
        results = self.__fetch_all()      
        similarities = []
        for id, emb, shape, layer in results:
            #takes the embedding that was put in as a string and makes a list of comma seperated numbers and turns them to be floats
            #it is then rehaped after being made into an np array to its original shape
            #eval takes the shape which is a string that looks like a tuple and turns into a real tuple again and reshapes on that
            emb_array = np.array([float(x) for x in emb.split(',')]).reshape(eval(shape))
            
            if emb_array.shape != query_shape:
                print(f"Warning: Embedding shape mismatch. Query: {query_shape}, Stored: {emb_array.shape}")
                continue
            #this is how cosine similiarity is done, take dot product of both embeddings and divide by the euclidean norm of both multiplied
            similarity = np.dot(query_embedding, emb_array) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb_array))
            similarities.append((id, similarity, layer))
        
        if not similarities:
            print("No valid embeddings found for comparison.")
            return []
        
        # Sort by similarity and then by layer (preferring lower layers for equal similarity)
        #sorted by similiarity and if they are the same takes the layer in desecending order which is why layer is negative thats why reverse=true for descending
        top_ids = sorted(similarities, key=lambda x: (x[1], -x[2]), reverse=True)[:top_k]
        
        return self.__find_similiarities(top_ids)
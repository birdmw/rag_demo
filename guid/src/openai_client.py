from config import OPENAI_API_KEY
from openai import OpenAI
import numpy as np
import time
import requests
from requests.exceptions import Timeout

class Gpt:

    def __init__(self) -> None:
         self.client = OpenAI(api_key=OPENAI_API_KEY)
         self.encoder = "text-embedding-ada-002"
         self.system_message = """You are an AI assistant tasked with answering questions about a healthcare plan offered by a healthcare company based on provided context. Use the given information to answer the question accurately and concisely."""
         self.system_no_rag = "act as you normally would, you are not allowed to search using the web at all"

    def rag_checkbox(self, user_message):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_no_rag},
                    {"role": "user", "content": user_message}
                ]
            )
         
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error in generating final answer: {e}")
            return "Unable to generate a final answer due to an error."

    def summarize_pair(self, chunk1, chunk2):
        system_message = "You are an AI assistant tasked with summarizing text. Provide a concise summary that captures the key points of the given text."
        user_message = f"Summarize the following text:\n\n{chunk1}\n\n{chunk2}"
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()  

    def encode_text(self, text, max_retries=10, backoff_factor=2, timeout=30):
        for attempt in range(max_retries):
            try:
                response = self.client.embeddings.create(
                    model=self.encoder,
                    input=[text],
                    timeout=timeout
                )

                embedding = np.array(response.data[0].embedding)
                return embedding, embedding.shape
            
            except Timeout:
                wait_time = backoff_factor * (2 ** attempt)
                print(f"Request timed out. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

            except Exception as e:
                wait_time = backoff_factor * (2 ** attempt)
                print(f"Error occurred: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
      
        raise Exception("Failed to encode text after all attempts") 
    
    def generate(self, context, query):
        user_message = f"""Context from healthcare plan document:

        {context}

        Based on this context, please answer the following question:
        {query}

        Provide a concise answer that directly addresses the question using only the information given in the context."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": user_message}
                ]
            )
            final_answer = response.choices[0].message.content.strip()
            return final_answer
        
        except Exception as e:
            print(f"Error in generating final answer: {e}")
            return "Unable to generate a final answer due to an error."
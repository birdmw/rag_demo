class Gpt:
    # this was chunking code which used openai api, it was cut from the openai_client.py file in the guid folder
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
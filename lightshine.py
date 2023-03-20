import json
import openai
import requests
with open("secrets.json") as f:
    secrets = json.load(f)
openai.api_key = secrets["OPENAI_API_KEY"]

class InspirationGenerator:
    def __init__(self):
        pass

    def ask_topic(self):
        """
        Prompts the user to enter a  self.topic and checks it for potential violations using the OpenAI content moderation API.

        Returns:
        - If the user enters an empty string, prints an error message and returns None.
        - If the prompt is flagged for a violation, prints a message indicating the category of violation and returns None.
        - If the prompt is not flagged for a violation, prints a message indicating that it has not been flagged and returns the  self.topic as a string.


        Raises:
        - requests.exceptions.RequestException: If the API request fails due to a network or other error.
        """
        self.topic = input("What  self.topic do you want to know about Jesus' thoughts? ")
        if  self.topic == '':
            print("Error: Please enter a valid  self.topic.")
            return None
        else:
            try:
                response = requests.post('https://api.openai.com/v1/moderations',
                    json={
                        "input":  self.topic
                    },
                    headers={
                        "Authorization": "Bearer "+ openai.api_key,
                        "Content-Type": "application/json"
                    })
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error: API request failed with exception {e}")
                return None
            
            data = response.json()
            flagged = data['results'][0]['flagged']
            if flagged:
                categories = data['results'][0].get('categories', {})
                true_category = next((k for k, v in categories.items() if v), None)
                print(f"The  self.topic has been flagged for {true_category}.")
                return None
            else:
                print("The prompt has not been flagged")
            return  self.topic
    
    def create_prompt(self):
        with open("prompt.json") as f:
            prompt_parts = json.load(f)
            prompt = prompt_parts['begin'] +  " " + self.topic + ". " + prompt_parts['end']
        return prompt
    
    def generate(self,prompt):
        response = openai.Completion.create(engine="text-davinci-003",
                                                    prompt=prompt,
                                                    max_tokens=600,
                                                    temperature=0.7)
        return response
                
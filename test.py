import openai
import os

# Set the API key
from dotenv import load_dotenv
load_dotenv()
# Retrieve the API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Use the ChatGPT model to generate text
model_engine = 'text-davinci-002'
prompt = 'Hello, how are you today?'
completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1,stop=None,temperature=0.7)
message = completion.choices[0].text
print(message)


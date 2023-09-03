import openai
import os
'''
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
'''
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
chain = load_summarize_chain(llm, chain_type="stuff")

chain.run(docs)

'''
Extracts the directories given and creates the contextual background of 
the instantiated GPT-Mind Persona.
Stores said context in /data, under the subdirectory of Persona name
'''
from PyPDF2 import PdfReader
from docx import Document
import os
import json
import sys

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain


def display_progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '-' * int(round(progress * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f'\rProgress: [{arrow + spaces}] {int(progress * 100)}%')
    sys.stdout.flush()


# Content Extraction Class
class ContentExtractor:
    def __init__(self, directory):
        self.context_dir = directory


    def extract_content(self, dir_name):
        total_files = sum([len(files) for subdir, _, files in os.walk(self.context_dir)])
        processed_files = 0

        # Ensure the data directory and subdirectory exist
        self.data_dir = os.path.join('src/data', dir_name)
        os.makedirs(self.data_dir, exist_ok=True)
        context_dir = os.path.join(self.data_dir, 'context.json')

        # Open the JSON file and write the opening curly brace
        with open(context_dir, 'w') as json_file:
            json_file.write("{\n")

        first_entry = True

        for subdir, _, files in os.walk(self.context_dir):  # Recursively walk through all files and subdirectories
            for file in files:
                file_path = os.path.join(subdir, file)
                file_content = self.extract_file(file_path)

                # Construct the JSON entry for this file
                json_entry = json.dumps({file_path: file_content}, indent=4)

                # If this isn't the first entry, prepend a comma
                if not first_entry:
                    json_entry = ",\n" + json_entry
                else:
                    first_entry = False

                # Append the JSON entry to the file
                with open(context_dir, 'a') as json_file:
                    json_file.write(json_entry)

                processed_files += 1
                display_progress_bar(processed_files, total_files)

        # Write the closing curly brace to the JSON file
        with open(context_dir, 'a') as json_file:
            json_file.write("\n}")


    def extract_file(self, file_path):
        text = None
        # Use python-magic to determine file type
        _, file_extension = os.path.splitext(file_path)

        if file_extension == ".pdf":                            # PDF
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()

        elif file_extension == ".docx":                         # Word
            doc = Document(file_path)
            fullText = []
            for paragraph in doc.paragraphs:
                fullText.append(paragraph.text)
            text = '\n'.join(fullText)

        elif file_extension == ".txt":                          # Txt
            with open(file_path, 'r') as file:
                text = file.read()

        return text
    

    def extract_summary(self):
        # Load the detailed_context.json file
        with open(os.path.join(self.data_dir, 'context.json'), 'r') as file:
            detailed_context = json.load(file)

        summarized_context = {}

        for key, content in detailed_context.items():
            summarized_context[key] = self._summarize_map_reduce(content)

        # Save the summarized content to summarized_context.json
        with open(os.path.join(self.data_dir, 'summaries.json'), 'w') as file:
            json.dump(summarized_context, file, indent=4)

    def _summarize_map_reduce(self, content):
        prompt_template = """Write a concise summary of the following:
        "{text}"
        CONCISE SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

        return stuff_chain.run(content)
        

if __name__ == '__main__':
    from time import time
    start = time()
    print('\nStart Context.py')

    Extractor = ContentExtractor(r'C:\Users\infor\OneDrive\Jeff\Cambridge\IIB Project - RNN\Readings')
    Extractor.data_dir = r'C:\Users\infor\Desktop\gpt-mind\src\data\RNN_Readings'
    Extractor.extract_summary()

    print(f'\nRuntime = {round(time()-start,1)}')


            




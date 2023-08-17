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

def display_progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '-' * int(round(progress * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f'\rProgress: [{arrow + spaces}] {int(progress * 100)}%')
    sys.stdout.flush()


# Content Extraction Class
class ContentExtractor:
    def __init__(self, directory):
        self.directory = directory


    def extract_content(self, dir_name):
        total_files = sum([len(files) for subdir, _, files in os.walk(self.directory)])
        processed_files = 0

        # Ensure the data directory and subdirectory exist
        os.makedirs(os.path.join('src/data', dir_name), exist_ok=True)
        json_path = os.path.join('src/data', dir_name, 'context.json')
        
        # Create or reset the file at the beginning
        with open(json_path, 'w') as json_file:
            json_file.write("{\n")
        
        for subdir, _, files in os.walk(self.directory):  # Recursively walk through all files and subdirectories
            for file in files:
                file_path = os.path.join(subdir, file)
                file_content = self.extract_file(file_path)
                if file_content:
                    with open(json_path, 'a') as json_file:
                        json.dump({file_path: file_content}, json_file)
                        json_file.write(",\n")  # Preparing for the next record
                    
                processed_files += 1
                display_progress_bar(processed_files, total_files)

        # Closing the last comma and enclosing the JSON content
        with open(json_path, 'rb+') as file:
            file.seek(-2, os.SEEK_END)  # Seek the position to the last comma
            file.truncate()  # Remove the last comma
            file.write(b"\n}")  # Close the JSON content


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
        

if __name__ == '__main__':
    from time import time
    start = time()
    print('\nStart Content Extraction')

    Extractor = ContentExtractor(r'C:\Users\infor\OneDrive\Jeff\Cambridge\IIB Project - RNN\Readings')
    Extractor.extract_content('RNN Readings')

    print(f'\nRuntime = {round(time()-start,1)}')


            




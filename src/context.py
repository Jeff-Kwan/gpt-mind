'''
Extracts the directories given and creates the contextual background of 
the instantiated GPT-Mind Persona.
Stores said context in /data, under the subdirectory of Persona name
'''
import PyPDF2
from docx import Document
import magic


# Content Extraction Class
class ContentExtractor:
    def __init__(self, directory):
        self.directory = directory
        self.content = self.extract_content()

    def extract_content(self):
        # Implement self.extract_file for all files in given directory(ies)
        # Builds the context stored file in a txt document in /data
        # Perhaps put important points in cache so it accesses it faster?
        return 
    

    def extract_file(self, file_path):
        text = None
        # Use python-magic to determine file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)

        if "pdf" in file_type:                                  # PDF
            with open('path_to_pdf', 'rb') as file:
                reader = PyPDF2.PdfFileReader(file)
                text = ""
                for page_num in range(reader.numPages):
                    text += reader.getPage(page_num).extractText()

        elif "openxmlformats-officedocument" in file_type:      # Word
            doc = Document('path_to_docx')
            fullText = []
            for paragraph in doc.paragraphs:
                fullText.append(paragraph.text)
            text = '\n'.join(fullText)

        elif "text" in file_type:                               # Txt
            with open('path_to_txt', 'r') as file:
                text = file.read()

        return text
        

            


            




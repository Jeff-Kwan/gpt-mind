'''
Instantiates GPT-Mind Persona.
'''
import os, json

from context import ContentExtractor



class Persona:
    '''Persona class that chats with a directoryual background.'''
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory

    def create_context():
        # Checks if context is created, uses ContentExtractor to create it if not
        return

    def respond(self, query):
        # Use the content & LangChain (or any other chatbot framework) to generate a response
        # The content can be used to provide directory or reference for the response
        return 
    


class Persona_Management:
    def __init__(self):
        self.storage_file = 'data/personas.json'
        # Check and create the file if it doesn't exist
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as file:
                json.dump({}, file)

    # Load all personas from the storage file
    def load_all(self):
        with open('data/personas.json', 'r') as file:
            return json.load(file)

    # Create a new persona
    def create(self, name, directory):
        personas = self.load_all()
        personas[name] = {"directory": directory}
        with open('data/personas.json', 'w') as file:
            json.dump(personas, file)

    # Delete an existing persona
    def delete(self, name):
        personas = self.load_all()
        if name in personas:
            del personas[name]
            with open('data/personas.json', 'w') as file:
                json.dump(personas, file)

    # Load and returns a specific Persona
    def load_persona(self, name):
        personas = self.load_all()
        if name in personas:
            return Persona(name, personas[name]["directory"]) 
        else:
            print(f'Persona "{name}" is not instantiated.')
        return None
'''
Main file to run for GPT-Mind.
'''
from persona import Persona_Management

mastermind = Persona_Management()

# Create a new persona for poems
mastermind.create("Poem Assistant", "path_to_poem_directory")

# List all available personas
print(mastermind.load_all())

# Load an existing persona
mind = mastermind.load_persona("Poem Assistant")
if mind:
    response = mind.respond("Tell me about limericks with one!")
    print(response)

# Delete a personaa
mastermind.delete("Poem Assistant")

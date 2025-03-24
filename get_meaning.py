import requests
import json

import spacy
nlp = spacy.load('en_core_web_sm')

# Preload the dictionary to avoid loading it multiple times
with open("optimized_dictionary2.json", "r") as file:
    DICTIONARY = json.load(file)

# def get_meaning(word):
#     """
#     Returns: A list of string definitions for the given word if it exists.
#     """
#     while True:  # Keep retrying until a valid definition is found
#         url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             definitions = []
#             # Data is in a list so access list, then meanings
#             for meaning in data[0]['meanings']:
#                 # then each individual definition which we append to our definitions list
#                 for definition in meaning['definitions']:
#                     # if definition['definition'][0] == "W":  # Invalid definition
#                     #     print(f"Invalid definition for '{word}', retrying...")
#                     #     break  # Exit the inner loop and retry the API call
#                     definitions.append(definition['definition'])  # Extract the definition
#             if definitions:  # If valid definitions are found, return them
#                 return definitions
#         else:
#             # If the word is not found, try reducing it to its base form
#             base_word = reduce_to_base_form(word)
#             if base_word and base_word != word:
#                 print(f"Word '{word}' not found. Trying base form '{base_word}'...")
#                 word = base_word  # Retry with the base form
#             else:
#                 return [f"Word '{word}' not found"]  # Return a fallback message if no valid word is found

def get_meaning_locally(word):
    """
    Returns: A dictionary containing the part of speech, synonyms, and definitions for the given word if it exists.
    """

    word = word.lower()  # Convert the word to lowercase
    
    # Search for the word in the dictionary
    if word in DICTIONARY:
            return DICTIONARY[word]["definitions"]
    
    # Try reducing the word to its base form
    base_word = reduce_to_base_form(word)
    if base_word and base_word != word:
        print(f"Word '{word}' not found. Trying base form '{base_word}'...")
        return get_meaning_locally(base_word)  # Return the result of the recursive call
    
    # If the word is not found, return a fallback message
    print(f"Word '{word}' not found.")
    return None

def reduce_to_base_form(word):
    """
    Reduces a word to its base form by removing common suffixes and applying lemmatization.
    """
    
    # First, try lemmatizing the word
    base_word = nlp(word)[0].lemma_
    if base_word != word:
        return base_word  # Return the lemmatized word if it's different

    # If lemmatization doesn't change the word, try removing common suffixes
    suffixes = ['ly', 'ing', 'ed', 'ness', 's', 'es', 'ment', 'able', 'al', 'ful', 'ous', 'tion']
    for suffix in suffixes:
        if word.endswith(suffix):
            stripped_word = word[:-len(suffix)]
            return stripped_word  # Return the stripped word if valid

    # If no suffix matches, return the original word
    return word

import requests

def get_meaning(word):
    """
    Returns: A list of string definitions for the given word if it exists.
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        definitions = []
        # Data is in a list so access list, then meanings
        for meaning in data[0]['meanings']:
            # then each individual definition which we append to our definitions list
            for definition in meaning['definitions']:
                definitions.append(definition['definition'])  # Extract the definition
        return definitions
    else:
        # If the word not found, try base_word to remove prefixes
        base_word = reduce_to_base_form(word)
        if base_word and base_word != word:
            print(f"Word '{word}' not found. Trying base form '{base_word}'...")
            return get_meaning(base_word)
        else:
            return (f"Word {word} not found")
        
def reduce_to_base_form(word):
    """
    Returns: A list of string definitions for the given word if it exists.
    """
    # List of common suffixes to strip
    suffixes = ['ly']
    for suffix in suffixes:
        # endswith checks the end of a string
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word  # Return the original word if no suffix matches
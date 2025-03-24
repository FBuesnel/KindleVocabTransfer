import json

def optimize_dictionary(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Convert the list of entries into a key-value dictionary
    optimized_data = {entry["word"].lower(): {"definitions": entry["definitions"]} for entry in data}

    # Save the optimized dictionary to a new file
    with open(output_file, 'w') as file:
        json.dump(optimized_data, file, indent=4)

    print(f"Optimized dictionary saved to {output_file}")

# Input and output file paths
input_file = "dictionary.json"
output_file = "optimized_dictionary.json"

# Run the optimization
optimize_dictionary(input_file, output_file)

# Optimize dictionary_array.json to optimized_dictionary2.json
input_file = "dictionary_array.json"
output_file = "optimized_dictionary2.json"
def optimize_dictionary_array(input_file, output_file):
    with open(input_file, 'r') as file:
        # Load the JSON data
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    # Ensure the data is a list
    if not isinstance(data, list):
        raise ValueError("Expected a list in the input JSON file.")

    # Convert the list of key-value pairs into the desired optimized format
    optimized_data = {}
    for entry in data:
        for word, definition in entry.items():
            optimized_data[word.lower()] = {"definitions": [definition]}

    # Save the optimized dictionary to a new file
    with open(output_file, 'w') as file:
        json.dump(optimized_data, file, indent=4)

    print(f"Optimized dictionary saved to {output_file}")

optimize_dictionary_array("dictionary_array.json", "optimized_dictionary2.json")
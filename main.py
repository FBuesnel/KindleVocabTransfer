import sqlite3
import csv
import get_meaning
import os
import json
import openpyxl
from tkinter import Tk
from tkinter.filedialog import askdirectory

def select_kindle_folder():
    """
    Opens a dialog for the user to select the Kindle folder.
    Returns the path to the Kindle folder.
    """
    Tk().withdraw()  # Hide the root Tkinter window
    kindle_folder = askdirectory(title="Select Your Kindle Folder")
    if not kindle_folder:
        raise FileNotFoundError("No folder selected. Please select the Kindle folder.")
    return kindle_folder

def connect_to_kindle_db(kindle_folder):
    """
    Connects to the Kindle database located in the selected folder.
    Returns the SQLite connection and cursor.
    """
    db_path = f"{kindle_folder}/system/vocabulary/vocab.db"  # Path to the Kindle database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print(f"Connected to database at: {db_path}")
    return conn, c

def read_book_titles_with_usages(c):
    c.execute('SELECT l.word_key, l.usage, b.title, b.authors '
              'FROM LOOKUPS l, BOOK_INFO b '
              'WHERE b.id = l.book_key '
              'ORDER BY l.word_key')
    result = []
    for row in c.fetchall():
        # Modify the first column (word_key) by removing the first three characters
        _, word = row[0].split(":")  # Remove the first three characters from word_key which contains
        try:
            definition = get_meaning.get_meaning_locally(word)[0]  # Get the first definition
        except (IndexError, TypeError):
            definition = "Definition not found"  # Fallback if no definition is returned
        # Create a new tuple with the definition as the second element
        modified_row = (word, definition) + row[1:]
        result.append(modified_row)  # Add the modified row to the result list
    return result

# Ensure the output folder exists
OUTPUT_FOLDER = "output"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def write_to_csv(c, result):
    with open(os.path.join(OUTPUT_FOLDER, 'vocab.csv'), 'w', newline='') as csvfile:
        # Open CSV writer
        w = csv.writer(csvfile, delimiter=' ')

        # Write header row to the CSV file
        w.writerow(['Word', 'Definition, Usage, Book Title, Authors'])

        for row in result:
            word = row[0]
            definition = row[1]  # Use the definition from the result
            usage = row[2]
            book_title = row[3]
            author = row[4]

            # Format the output
            formatted_output = f"{definition}\n\n{usage}\nFrom {book_title} by {author}"

            # Write the word and formatted output to the CSV
            w.writerow([word, formatted_output])

    print("CSV write successful")

def write_to_json(c, result):
    data = []

    for row in result:
        word = row[0]
        definition = row[1]  # Use the definition from the result
        usage = row[2]
        book_title = row[3]
        author = row[4]

        # Create a dictionary for each word
        entry = {
            "word": word,
            "definition": definition,
            "usage": usage,
            "book_title": book_title,
            "author": author
        }
        data.append(entry)

    # Write to a JSON file
    with open(os.path.join(OUTPUT_FOLDER, 'vocab.json'), 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    print("JSON write successful")

def write_to_excel(c, result):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Vocabulary"

    # Write header row
    ws.append(['Word', 'Definition', 'Usage', 'Book Title', 'Author'])

    for row in result:
        word = row[0]
        definition = row[1]  # Use the definition from the result
        usage = row[2]
        book_title = row[3]
        author = row[4]

        # Write each row to the Excel sheet
        ws.append([word, definition, usage, book_title, author])

    wb.save(os.path.join(OUTPUT_FOLDER, 'vocab.xlsx'))
    print("Excel write successful")

def write_to_html(c, result):
    with open(os.path.join(OUTPUT_FOLDER, 'vocab.html'), 'w') as htmlfile:
        htmlfile.write('<html><body><h1>Vocabulary</h1><table border="1">')
        htmlfile.write('<tr><th>Word</th><th>Definition</th><th>Usage</th><th>Book Title</th><th>Author</th></tr>')

        for row in result:
            word = row[0]
            definition = row[1]  # Use the definition from the result
            usage = row[2]
            book_title = row[3]
            author = row[4]

            # Write each row as an HTML table row
            htmlfile.write(f'<tr><td>{word}</td><td>{definition}</td><td>{usage}</td><td>{book_title}</td><td>{author}</td></tr>')

        htmlfile.write('</table></body></html>')

    print("HTML write successful")

def clear_db(c, conn):
    try:
        c.execute('DELETE FROM LOOKUPS')
        c.execute('DELETE FROM BOOK_INFO')
        c.execute('DELETE FROM WORDS')
        conn.commit()  # Commit the changes to the database
        print("Database cleared successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error clearing the database: {e}")

WRITING_FUNCTIONS = [write_to_csv, write_to_json, write_to_excel, write_to_html]

def main():
    try:
        # Let the user select the Kindle folder
        # kindle_folder = select_kindle_folder()

        # Connect to the Kindle database
        # conn, c = connect_to_kindle_db(kindle_folder)
        conn = sqlite3.connect("vocab.db")
        c = conn.cursor()


        # Perform operations
        result = read_book_titles_with_usages(c)
        for write_function in WRITING_FUNCTIONS:
            write_function(c, result)

        ### THIS WILL CLEAR IT, BE CAREFUL ###
        # clear_db(c, conn)

        # Close the connection
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # Execute only if run as the entry point into the program
    main()
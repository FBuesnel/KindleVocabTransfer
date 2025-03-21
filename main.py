import sqlite3
import csv
import get_meaning
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
              'ORDER BY b.authors')
    result = []
    for row in c.fetchall():
        # Modify the first column (word_key) by removing the first three characters
        modified_row = (row[0][3:],) + row[1:]  # Create a new tuple with the modified word_key
        result.append(modified_row)  # Add the modified row to the result list
    return result

def write_to_csv(c):
    with open('vocab.csv', 'w', newline='') as csvfile:
        # Open CSV writer
        w = csv.writer(csvfile, delimiter=' ')
        result = read_book_titles_with_usages(c)

        # Write header row to the CSV file
        w.writerow(['Word', 'Definition, Usage, Book Title, Authors'])

        for row in result:
            word = row[0]
            definition = get_meaning.get_meaning(word)[0]  # Get the first definition
            usage = row[1]
            book_title = row[2]
            author = row[3]

            # Format the output
            formatted_output = f"{definition}\n\n{usage}\nFrom {book_title} by {author}"

            # Write the word and formatted output to the CSV
            w.writerow([word, formatted_output])

    print("CSV write successful")

def clear_db(c, conn):
    try:
        c.execute('DELETE FROM LOOKUPS')
        c.execute('DELETE FROM BOOK_INFO')
        c.execute('DELETE FROM WORDS')
        conn.commit()  # Commit the changes to the database
        print("Database cleared successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error clearing the database: {e}")

def main():
    try:
        # Let the user select the Kindle folder
        kindle_folder = select_kindle_folder()

        # Connect to the Kindle database
        conn, c = connect_to_kindle_db(kindle_folder)

        # Perform operations
        write_to_csv(c)
        # clear_db(c, conn)

        # Close the connection
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # Execute only if run as the entry point into the program
    main()
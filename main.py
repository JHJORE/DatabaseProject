import sqlite3
import database

conn = sqlite3.connect('theater.db')  # This creates or opens the database file
cursor = conn.cursor()
cursor.execute('''Fill''')  
conn.commit()  # Commit changes to the database


if __name__ == "__main__":
    

import sqlite3
import database
import CLI as interface



conn = sqlite3.connect('theater.db')  # This creates or opens the database file
cursor = conn.cursor()
cursor.execute('''Fill''')  
conn.commit()  

if __name__ == "__main__":
    interface.main_menu()
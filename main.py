import sqlite3
import database
import CLI as interface
import database as datab
import crud as c
datab.initialize_db()

if __name__ == "__main__":
    conn = sqlite3.connect('theater.db')
    cursor = conn.cursor()
    
    print(c.get_names_of_actors_in_various_playes(conn))
    
    

    
   
  
   
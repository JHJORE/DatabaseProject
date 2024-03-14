import sqlite3
import database
import CLI as interface
import database as datab
import crud 

datab.initialize_db()

if __name__ == "__main__":
    
    pass
   # interface.main_menu()
    conn = sqlite3.connect('theater.db')
    cursor = conn.cursor()
    # crud.add_employee(conn, ["John", "joe@gmail.com","921234", "parttime"])
    #crud.add_actor(conn, 1)
    
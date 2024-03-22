import sqlite3
import database
import CLI as interface
import database as datab
import crud as c
import checkseat


if __name__ == "__main__":
    conn = sqlite3.connect("theater.db")
    cursor = conn.cursor()
    interface.main_menu(conn)
    

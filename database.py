import sqlite3

def connect_db():
    return sqlite3.connect('theater.db')

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    print("Connecting to Schema.sql")
    try:
        with open('schema.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)

            print('Database created and initialized successfully')

    except sqlite3.Error as e:
        print('Error:', e)

    finally:
        conn.commit()
        conn.close()



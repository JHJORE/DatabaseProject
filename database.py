import sqlite3
import pandas as pd


def connect_db():
    return sqlite3.connect("theater.db")


def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    print("Connecting to Schema.sql")
    try:
        with open("schema.sql", "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)

            print("Database created and initialized successfully")

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        conn.commit()
        conn.close()

def fill_db():
    conn = connect_db()
    cursor = conn.cursor()
    # Using csv file to fill the database
    folder_name = "csv_data/"
    
    # Fill employees table
    print("Filling employees table")
    employees_kongsemne = pd.read_csv(folder_name + "employees_kongsemnene_filled.csv")
    employees_stortst_av_alt = pd.read_csv(folder_name + "storst_av_alt_er_kjaerligheten_employees.csv")

    raise NotImplemented
    #finally:
    #    conn.commit()
    #    conn.close()


def flush_db():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Retrieve a list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Iterate over the list of tables and delete all records from each
        for table_name in tables:
            print(f"Flushing {table_name[0]}")
            cursor.execute(f"DELETE FROM {table_name[0]}")

        print("Database flushed successfully")
    except sqlite3.Error as e:
        print(f"Error flushing database: {e}")
    finally:
        conn.commit()
        conn.close()

import sqlite3
import pandas as pd
import crud


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
    employees_stortst_av_alt = pd.read_csv(
        folder_name + "storst_av_alt_er_kjaerligheten_employees.csv"
    )
    # Concatenate the two dataframes
    employees_all = pd.concat([employees_kongsemne, employees_stortst_av_alt])

    # Drop duplicates based on 'group' and 'Name' columns, keeping the first occurrence
    employees_all_unique = employees_all.drop_duplicates(
        subset=["group", "Name"], keep="first"
    )

    # fill employees table from the dataframe
    print(employees_all_unique.columns)
    employees_all_unique.apply(
        lambda row: crud.add_employee(
            conn, (row["Name"], row["Email"], row["Phone"], row["status"])
        ),
        axis=1,
    )

    # Fill theater halls table
    print("Filling theater halls table")
    theater_halls = pd.read_csv(folder_name + "theater_halls.csv")
    theater_halls.apply(
        lambda row: crud.add_theater_hall(conn, (row["Name"], row["capacity"])),
        axis=1,
    )

    # Fill Areas table
    print("Filling areas table")
    areas = pd.read_csv(folder_name + "seating_theater_halls.csv")
    areas["AreaID"] = (
        areas.groupby(["Name", "Area"]).ngroup() + 1
    )  # Create a unique ID for each area

    # get THID from theaterHalls table
    theater_halls = crud.get_all_theater_halls(conn)
    theater_halls = pd.DataFrame(theater_halls, columns=["THID", "Name", "capacity"])
    areas = pd.merge(areas, theater_halls, on="Name")
    areas = areas.drop_duplicates(
        subset=["THID", "AreaID"], keep="first"
    )  # Only keep unique combinations of THID and AreaID
    areas.apply(
        lambda row: crud.add_area(conn, (row["THID"], row["AreaID"], row["Area"])),
        axis=1,
    )

    """
    # Fill plays table
    print("Filling plays table")
    plays = pd.read_csv(folder_name + "plays.csv")
    plays.apply(
        lambda row: crud.add_play(
            conn, (row["title"], row["description"], row["duration"])
        ),
        axis=1,
    )
    """

    # finally:
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

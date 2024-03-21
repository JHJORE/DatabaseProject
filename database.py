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

    # Fill actors table
    print("Filling actors table")
    employees_all_unique_actors = crud.get_all_employees(conn)
    employees_all_unique_with_ID = pd.DataFrame(
        employees_all_unique_actors, columns=["EID", "Name", "Email", "Phone", "status"]
    )
    employees_all_unique_with_ID_and_group = pd.merge(
        employees_all_unique, employees_all_unique_with_ID, on="Name"
    )
    employees_all_unique_actors = employees_all_unique_with_ID_and_group[
        employees_all_unique_with_ID_and_group["group"] == "actor"
    ]
    employees_all_unique_actors.apply(
        lambda row: crud.add_actor(conn, (row["EID"])), axis=1
    )

    # Fill managers table
    print("Filling managers table")
    employees_all_from_database = crud.get_all_employees(conn)
    employees_all_from_database_with_ID = pd.DataFrame(
        employees_all_from_database, columns=["EID", "Name", "Email", "Phone", "status"]
    )
    # Attempt to add Yury Butusov as a manager
    try:
        manager_kongsemnene = employees_all_from_database_with_ID[
            employees_all_from_database_with_ID["Name"] == "Yury Butusov"
        ]
        crud.add_manager(conn, int(manager_kongsemnene["EID"].iloc[0]))
    except IndexError:
        print("Manager Yury Butusov not found.")

    # Attempt to add Jonas Corell Petersen as a manager
    try:
        manager_storst_av_alt = employees_all_from_database_with_ID[
            employees_all_from_database_with_ID["Name"] == "Jonas Corell Petersen"
        ]
        crud.add_manager(conn, int(manager_storst_av_alt["EID"].iloc[0]))
    except IndexError:
        print("Manager Jonas Corell Petersen not found.")

    # Fill TheaterPlay table
    print("Filling TheaterPlay table")
    theater_plays = pd.read_csv(folder_name + "plays.csv")
    theater_plays_with_THID = pd.merge(
        theater_plays,
        theater_halls.rename(columns={"Name": "theaterHallName"}),
        on="theaterHallName",
    )

    theater_plays_with_THID.apply(
        lambda row: crud.add_theater_play(
            conn, (row["season"], row["Name"], row["THID"])
        ),
        axis=1,
    )

    # Fill ManagerOf table
    print("Filling ManagerOf table")
    all_plays = crud.get_all_theater_plays(conn)
    theater_plays_with_THID_and_manager_EID = pd.DataFrame(
        all_plays, columns=["PlayID", "season", "Name", "THID", "EID"]
    )
    theater_plays_with_THID_and_manager_EID["EID"] = ""

    # Loop through the DataFrame and set EID based on the play's name
    for index, row in theater_plays_with_THID_and_manager_EID.iterrows():
        if row["Name"] == "Størst av alt er kjærligheten":
            theater_plays_with_THID_and_manager_EID.at[index, "EID"] = int(
                manager_storst_av_alt["EID"].iloc[0]
            )
        if row["Name"] == "Kongsemnene":
            theater_plays_with_THID_and_manager_EID.at[index, "EID"] = int(
                manager_kongsemnene["EID"].iloc[0]
            )
    theater_plays_with_THID_and_manager_EID.apply(
        lambda row: crud.add_manager_of(conn, (row["EID"], row["Name"])), axis=1
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

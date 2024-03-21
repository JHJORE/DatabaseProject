import sqlite3
import pandas as pd
import crud as c
import csv


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
    #Using csv file to fill the database
    # make_theater_hall(conn)
    # print("Theater hall filled")
    # make_theater_play(conn)
    # print("Theater play filled")
    # make_customer_segments(conn)
    # print("Customer segments filled")
    # make_performace(conn)
    # print("Performance filled")
    # make_main_stage_seating(conn)
    # print("Main stage seating filled")
    # make_old_stage_seating(conn)
    # print("Old stage seating filled")
    # make_employees(conn)
    # print("Employees filled")
    # make_act(conn)
    # print("Act filled")
    make_act_other



def make_theater_hall(conn):
    with open("jjcvs_data/theater_halls.csv", 'r') as file:
        csv_reader = csv.reader(file)  # Pass the file object here
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if len(row) >= 2:  # Ensure the row has at least two elements
                name = row[0]
                capacity = int(row[1])  
                theater_hall = (name, capacity)
                c.add_theater_hall(conn, theater_hall)  
            else:
                print(f"Row skipped due to insufficient columns: {row}")

def make_theater_play(conn):
     with open("jjcvs_data/theater_plays.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  
        for row in csv_reader:
            if len(row) >= 3:  # Ensure the row has at least three elements
                season = row[0]
                name = row[1]
                hallname = row[2]
                print(hallname)
                thid = c.get_theater_hall_by_name(conn, hallname)[0]
               # Correctly capture the return value without print()
                theater_play = (season, name, thid)
                c.add_theater_play(conn, theater_play)  # Now we can uncomment this to add the play
            else:
                print(f"Row skipped due to insufficient columns: {row}")

def make_customer_segments(conn):
    unique_segments = set()

    with open("jjcvs_data/ticket_prices.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  
        
        for row in csv_reader:
            play = row[0]
            segment = row[1]
            price = row[2]

            # Check if the segment has already been processed
            if segment not in unique_segments:
                unique_segments.add(segment)
                c.add_customer_group(conn, segment)

            playid = c.get_theater_play_by_name(conn, play)[0]
            
            # Assuming get_customer_group_by_segmentid is meant to retrieve segment id from the database
            segmentid = c.get_customer_group_by_segment(conn, segment)[0]

            group = (playid, segmentid, price)
    
            c.add_has_group(conn, group)

def make_performace(conn):
    with open("jjcvs_data/play_schedule.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  
        for row in csv_reader:
            play = row[0]
            date = row[1]
            time = row[2]
            playid = c.get_theater_play_by_name(conn, play)[0]
            performance = (date, time, playid)
            c.add_performance(conn, performance)

def make_main_stage_seating(conn,):
    unique_area = set()
    with open("jjcvs_data/main_stage_seating.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            place = row[0]
            row_number = row[1]  
            seat_number = row[2]
            
            # Use a combined key of place and thid to ensure uniqueness across executions
            thid = c.get_theater_hall_by_name(conn, "Main Stage")[0]
            unique_key = (place, thid)
            
            if unique_key not in unique_area:
                unique_area.add(unique_key)
                
                # Check if the area already exists in the database to avoid unique constraint errors. Had to do this becasue for some reason the set was not enough and we kept on getting errors
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM Area WHERE Name=? AND THID=?", (place, thid))
                exists = cur.fetchone()
                
                if not exists:
                    area = (thid, place)
                    c.add_area(conn, area)

            chair = (thid, place, seat_number, row_number)
            c.add_chair(conn, chair)
            
def make_old_stage_seating(conn,):
    unique_area = set()
    with open("jjcvs_data/old_stage_seating.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  
        for row in csv_reader:
            place = row[0]
            row_number = row[1]  
            seat_number = row[2]
            
            # Use a combined key of place and thid to ensure uniqueness across executions
            thid = c.get_theater_hall_by_name(conn, "Old Stage")[0]
            unique_key = (place, thid)
            
            if unique_key not in unique_area:
                unique_area.add(unique_key)
                
                # Check if the area already exists in the database to avoid unique constraint errors. Had to do this becasue for some reason the set was not enough and we kept on getting errors
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM Area WHERE Name=? AND THID=?", (place, thid))
                exists = cur.fetchone()
                
                if not exists:
                    area = (thid, place)
                    c.add_area(conn, area)

            chair = (thid, place, seat_number, row_number)
            c.add_chair(conn, chair)

def make_employees(conn):
    with open("jjcvs_data/employees.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            play = row[0]
            name = row[1]  
            email = row[2]
            status = row[3]
            task = row[4]
            employee = (name, email, status, task)
            
            # Add employee
            c.add_employee(conn, employee)
            eid = c.get_employee_by_name(conn, name)[0]
            playid = c.get_theater_play_by_name(conn, play)[0] if play else None
            
            if task == "Skuespiller":
                # Use get_actor_by_eid here as an example
                if not c.get_actor_by_eid(conn, eid):
                    c.add_actor(conn, eid)
                    if playid:
                        c.add_assigned_role(conn, (eid, playid))

            elif task == "Direktør":
                # Use get_manager_by_eid here as an example
                if not c.get_manager_by_eid(conn, eid):
                    c.add_manager(conn, eid)
                    if playid:
                        managerof = (eid, playid)
                        c.add_manager_of(conn, managerof)

            else:  # Assuming this is for backstage employees
                # Use get_backstage_employee_by_eid here as an example
                if not c.get_backstage_employee(conn, eid):
                    c.add_backstage_employee(conn, eid)
                    if playid:
                        backstage = (eid, playid, task)
                        c.add_assigned_backstage(conn, backstage)


def make_acts_saaek(conn):
    with open("jjcvs_data/SAAEK_act.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            playname = row[0]
            rolename = row[1]
            actnum = row[2]
            actname = row[3]


            playid = c.get_theater_play_by_name(conn, playname)[0]
            c.add_part_of(conn, )

def make_act(conn):
    act_names = [
        "Sverdet",
        "Bjørnejakt",
        "Brylluppet på Bergenhus",
        "Morgengave",
        "Manns minne",
        "Hoved",
    ]

    # Iterate over the act names with their index
    for i, act_name in enumerate(act_names, start=1):
        c.add_act(conn, act_name)
        if act_name == "Hoved":
           
            # playid = c.get_theater_play_by_name(conn, "Størst av alt er kjærligheten")[0]
            c.add_part_of(conn,i, 2)
        else:
            playid = c.get_theater_play_by_name(conn, "Kongsemnene")[0]
            c.add_part_of(conn, i, 1)


def make_act_kongsnemnd(conn):
     with open("jjcvs_data/kongsnemnd_act.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            playname = row[0]
            rolename = row[1]
            actnum = row[2]
            actname = row[3]
     

def make_act_other(conn):
    seen_roles = set()
    with open("jjcvs_data/SAAEK_act.csv", 'r') as file:
        csv_reader = csv.reader(file)  
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            playname = row[0]
            rolename = row[1]
            actnum = row[2]
            actname = row[3]
            if rolename not in seen_roles:
                # If not, add it to the database and the set of seen roles
                c.add_role(conn, rolename)
                seen_roles.add(rolename)
                numid = c.get_act_by_name(conn, actname)[0]
                roleid = c.get_role_by_name(conn, rolename)[0]
                c.add_role_in_act(conn, numid,roleid) 
            

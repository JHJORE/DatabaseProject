import os
import time
import subprocess
import database
import crud
import pandas as pd


def clear_screen():
    # For Windows
    if os.name == "nt":
        subprocess.run(["cls"], shell=True, check=True)
    # For macOS and Linux
    else:
        subprocess.run(["clear"], shell=True, check=True)


def main_menu():
    # connect to database
    conn = database.connect_db()
    cursor = conn.cursor()
    logged_off = False
    while not logged_off:
        print(
            """
            1. Initialize Database and Insert Initial Data
            2. Insert data
            3. Check Chair Availability
            4. Buy Tickets
            5. Find Actors by Play by date
            6. What actors are playing in a given play
            7. Most popular play
            8. Find co-actors for a given actor
            9. Exit
            """
        )

        choice = input("Enter your choice: ")

        if choice == "1":
            database.initialize_db()

        elif choice == "2":
            # Insert data
            pass
        elif choice == "3":
            # Check Chair Availability
            # check_chair_availability(conn)
            # Read data from the text files
            tickets_gs = process_seat_file(
                "files needed/gamle-scene.txt",
                "Storst av alt er kjærligheten",
                "Gamle Scene",
            )
            tickets_hs = process_seat_file(
                "files needed/hovedscenen.txt", "Kongsemnene", "Hovedscenen"
            )
            tickets = tickets_gs + tickets_hs
            for ticket in tickets:
                print(ticket)
        elif choice == "4":
            # Buy Tickets
            pass
        elif choice == "5":
            # 4. Find performances and ticket sales by date
            # get dates for the play
            date_times_kong = crud.get_play_dates_times(conn, "Kongsemnene")
            date_times_kong_df = pd.DataFrame(date_times_kong, columns=["Date", "Time"])
            date_times_storst = crud.get_play_dates_times(
                conn, "Storst av alt er kjærligheten"
            )
            date_times_storst_df = pd.DataFrame(
                date_times_storst, columns=["Date", "Time"]
            )
            date_times = pd.concat([date_times_kong_df, date_times_storst_df])

            # Get unique dates
            dates = date_times["Date"].unique()

            pass
        elif choice == "6":
            actors_and_roles = get_actors_and_roles(conn)
            for play, actor, role in actors_and_roles:
                print(f"{actor} is playing {role} in {play}")
        elif choice == "7":
            # 6. Most popular play

            best_selling_performances = get_best_selling_performances(conn)

            # Print the results
            for play_name, date, tickets_sold in best_selling_performances:
                print(f"Play: {play_name}, Date: {date}, Tickets Sold: {tickets_sold}")

        elif choice == "8":
            # 8. Find co-actors for a given actor for a given actor
            actor_name = "Your Actor's Name Here"  # Replace with the name of the actor you're interested in
            coactors = find_coactors_by_actor_name(conn, actor_name)

            for actor1, actor2, play_name in coactors:
                print(f"{actor1} and {actor2} played together in {play_name}")
        elif choice == "9":
            print("Exiting...")
            logged_off = True
        else:
            print("Invalid choice. Please choose again.")


def get_best_selling_performances(conn):
    """
    Fetches performances sorted by the number of seats sold in descending order.

    Parameters:
    - conn: SQLite database connection object

    Returns:
    - A list of tuples containing (PlayName, Date, TicketsSold)
    """
    sql = """
    SELECT 
        TheaterPlay.Name AS PlayName,
        Performance.Date,
        COUNT(Ticket.TicketID) AS TicketsSold
    FROM 
        Ticket
    JOIN 
        Performance ON Ticket.PerformanceID = Performance.PerformanceID
    JOIN 
        TheaterPlay ON Performance.PlayID = TheaterPlay.PlayID
    GROUP BY 
        Performance.PerformanceID
    ORDER BY 
        TicketsSold DESC, Performance.Date;
    """
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    return results


def get_performances_and_ticket_sales_by_date(conn, date):
    """
    Prints out performances on a given date and the number of tickets sold for each.

    Parameters:
    - conn: SQLite database connection object
    - date: The date for which to fetch performances and ticket sales (format: YYYY-MM-DD)
    """
    sql = """
    SELECT 
        TheaterPlay.Name AS PlayName,
        Performance.Date,
        IFNULL(COUNT(Ticket.TicketID), 0) AS TicketsSold
    FROM 
        Performance
    LEFT JOIN 
        Ticket ON Performance.PerformanceID = Ticket.PerformanceID
    JOIN 
        TheaterPlay ON Performance.PlayID = TheaterPlay.PlayID
    WHERE 
        Performance.Date = ?
    GROUP BY 
        Performance.PerformanceID
    ORDER BY 
        PlayName;
    """
    cur = conn.cursor()
    cur.execute(sql, (date,))
    results = cur.fetchall()

    if results:
        for play_name, date, tickets_sold in results:
            print(f"Play: {play_name}, Date: {date}, Tickets Sold: {tickets_sold}")
    else:
        print("No performances found for this date.")


def manage_theater_halls():

    print("Theater Hall Management")


def manage_plays():

    print("Play Management")


def manage_employees():

    print("Employee Management")


def find_coactors_by_actor_name(conn, actor_name):
    """
    Finds co-actors for the given actor name in the same act of plays.

    Parameters:
    - conn: SQLite database connection object
    - actor_name: The name of the actor

    Returns:
    - A list of tuples containing (Actor1, Actor2, PlayName)
    """
    sql = """
    SELECT DISTINCT
        e1.Name AS Actor1,
        e2.Name AS Actor2,
        tp.Name AS PlayName
    FROM
        Employees e1
    JOIN Actor a1 ON e1.EID = a1.EID
    JOIN RoleInAct ria1 ON a1.EID = ria1.NumID
    JOIN Acts ac1 ON ria1.NumID = ac1.NumID
    JOIN PartOf po1 ON ac1.NumID = po1.NumID
    JOIN TheaterPlay tp ON po1.PlayID = tp.PlayID
    JOIN PartOf po2 ON tp.PlayID = po2.PlayID
    JOIN Acts ac2 ON po2.NumID = ac2.NumID
    JOIN RoleInAct ria2 ON ac2.NumID = ria2.NumID
    JOIN Actor a2 ON ria2.NumID = a2.EID
    JOIN Employees e2 ON a2.EID = e2.EID
    WHERE e1.Name = ? AND e1.EID <> e2.EID;
    """
    cur = conn.cursor()
    cur.execute(sql, (actor_name,))
    results = cur.fetchall()
    return results


def process_seat_file(file_path, play_name, theater_hall_name):
    with open(file_path, "r") as file:
        lines = file.readlines()

    date = lines[0].strip().split()[1]  # Assumes the first line is always the date
    current_area = ""
    tickets = []

    for line in lines[1:]:
        line = line.strip()
        if line in [
            "Galleri",
            "Balkong",
            "Parkett",
        ]:  # Check if the line is an area name
            current_area = line
            row_no = 1  # Initialize row number for each area
        elif line:  # Non-empty line means seat row
            for seat_no, seat_status in enumerate(line, start=1):
                if seat_status == "1":  # Seat is occupied, create a ticket
                    tickets.append(
                        {
                            "theater_hall": theater_hall_name,
                            "play": play_name,
                            "date": date,
                            "area": current_area,
                            "row_no": row_no,
                            "seat_no": seat_no,
                        }
                    )
            row_no += 1  # Move to the next row after processing the current row

    return tickets


def get_actors_and_roles(conn):
    """
    Fetches the names of plays, actors, and their roles.

    Parameters:
    - conn: SQLite database connection object

    Returns:
    - A list of tuples containing (PlayName, ActorName, RoleName)
    """
    sql = """
    SELECT TheaterPlay.Name AS PlayName, Employees.Name AS ActorName, Role.Name AS RoleName
    FROM TheaterPlay
    JOIN PartOf ON TheaterPlay.PlayID = PartOf.PlayID
    JOIN Acts ON PartOf.NumID = Acts.NumID
    JOIN RoleInAct ON Acts.NumID = RoleInAct.NumID
    JOIN Role ON RoleInAct.RoleID = Role.RoleID
    JOIN Actor ON RoleInAct.NumID = Actor.EID
    JOIN Employees ON Actor.EID = Employees.EID;
    """
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    return results


def buy_tickets(conn):
    finished = False
    while not finished:
        play_picked = input(
            "What play do you want to buy tickets for?\n1: Kongsemnene (Playing in Hovedscenen) \n2: Storst av alt er kjærligheten (Playing in Gamle scene)\n:"
        )
        if play_picked == "1":
            play = "Kongsemnene"
        elif play_picked == "2":
            play = "Storst av alt er kjærligheten"
        else:
            print("Invalid choice. Please choose again.")
            continue

        # get dates for the play
        date_times = crud.get_play_dates_times(conn, play)
        date_times_df = pd.DataFrame(date_times, columns=["Date", "Time"])
        selected_date, selected_time = prompt_user_for_datetime_from_df(date_times_df)

        # find seats for the play
        if play == "Kongsemnene":
            theater_hall = "Hovedscenen"
            chosen_area = "Sal"
            rowNO = input("Enter row number: ")
            seatNO = input("Enter seat number: ")
        if play == "Storst av alt er kjærligheten":
            theater_hall = "Gamle Scene"
            chosen_area = prompt_user_for_area(conn, theater_hall)

        print("Checking chair availability...")
        time.sleep(2)
        if check_if_chair_occupied(
            conn,
            selected_date,
            selected_time,
            play,
            chosen_area,
            theater_hall,
            rowNO,
            seatNO,
        ):
            print("The chair is occupied, try again")
            continue
        else:
            print("The chair is available.\n")
            print("Do you want to buy a ticket for the specified time and chair?")
            choice = input("1: Yes\n2: No\n:")
            if choice == "1":
                # buy ticket logic
                pass
            elif choice == "2":
                finished = True
            else:
                print("Invalid choice. Please choose again.")
                continue
        input("Do you want to buy another ticket?\n1: Yes\n2: No\n:")
        if choice == "2":
            finished = True
        elif choice == "1":
            continue


def check_chair_availability(conn):
    finished = False
    while not finished:
        play_picked = input(
            "What play do you want to check?\n1: Kongsemnene (Playing in Hovedscenen) \n2: Storst av alt er kjærligheten (Playing in Gamle scene)\n:"
        )
        if play_picked == "1":
            play = "Kongsemnene"
        elif play_picked == "2":
            play = "Storst av alt er kjærligheten"
        else:
            print("Invalid choice. Please choose again.")
            break

        # get dates for the play
        date_times = crud.get_play_dates_times(conn, play)
        date_times_df = pd.DataFrame(date_times, columns=["Date", "Time"])
        selected_date, selected_time = prompt_user_for_datetime_from_df(date_times_df)

        # find seats for the play
        if play == "Kongsemnene":
            theater_hall = "Hovedscenen"
            chosen_area = "Sal"
            rowNO = input("Enter row number: ")
            seatNO = input("Enter seat number: ")
        if play == "Storst av alt er kjærligheten":
            theater_hall = "Gamle Scene"
            chosen_area = prompt_user_for_area(conn, theater_hall)

        print("Checking chair availability...")
        time.sleep(2)
        if check_if_chair_occupied(
            conn,
            selected_date,
            selected_time,
            play,
            chosen_area,
            theater_hall,
            rowNO,
            seatNO,
        ):
            print("The chair is occupied.")
        else:
            print("The chair is available.")

        print("Do you want to check another chair?")
        choice = input("1: Yes\n2: No\n:")
        if choice == "2":
            finished = True
        else:
            print("Invalid choice. Please choose again.")


def prompt_user_for_area(conn, hall_name):
    # Retrieve areas for the given hall name
    areas = crud.get_areas_in_hall(conn, hall_name)

    # Assuming 'areas' is a list of tuples like [(area_name,), (area_name,), ...]
    # If you have it in a different format, adjust the extraction logic accordingly

    # Display areas with an index
    print("Please choose an area by entering the corresponding number:")
    for i, area in enumerate(areas, 1):
        print(
            f"{i}: {area[0]}"
        )  # Assuming each tuple has the area name as its first element

    # Prompt user for area choice
    try:
        area_choice = int(input("Enter your choice for area: ")) - 1
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

    # Check if the choice is valid
    if 0 <= area_choice < len(areas):
        chosen_area = areas[area_choice][0]  # Extract the area name
    else:
        print("Invalid choice. Please try again.")
        return None

    return chosen_area


def prompt_user_for_datetime_from_df(date_times_df):
    # Get unique dates
    dates = date_times_df["Date"].unique()

    # Display dates with an index
    print("Please choose a date by entering the corresponding number:")
    for i, date in enumerate(dates, 1):
        print(f"{i}: {date}")

    # Prompt user for date choice
    date_choice = int(input("Enter your choice for date: ")) - 1

    # Check if the choice is valid
    if 0 <= date_choice < len(dates):
        chosen_date = dates[date_choice]
    else:
        print("Invalid date choice. Please try again.")
        return None, None

    # Filter times for the chosen date
    times_for_date = date_times_df.loc[
        date_times_df["Date"] == chosen_date, "Time"
    ].unique()

    # Display times with an index
    print("\nPlease choose a time by entering the corresponding number:")
    for i, time in enumerate(times_for_date, 1):
        print(f"{i}: {time}")

    # Prompt user for time choice
    time_choice = int(input("Enter your choice for time: ")) - 1

    # Check if the choice is valid
    if 0 <= time_choice < len(times_for_date):
        chosen_time = times_for_date[time_choice]
    else:
        print("Invalid time choice. Please try again.")
        return None, None

    return chosen_date, chosen_time


def prompt_user_for_date_from_df(date_times_df):
    # Get unique dates
    dates = date_times_df["Date"].unique()

    # Display dates with an index
    print("Please choose a date by entering the corresponding number:")
    for i, date in enumerate(dates, 1):
        print(f"{i}: {date}")

    # Prompt user for date choice
    date_choice = int(input("Enter your choice for date: ")) - 1

    # Check if the choice is valid
    if 0 <= date_choice < len(dates):
        chosen_date = dates[date_choice]
    else:
        print("Invalid date choice. Please try again.")
        return None

    return chosen_date


def check_if_chair_occupied(conn, date, time, play, area, hall_name, row_no, seat_no):
    sql = """
    SELECT EXISTS (
        SELECT 1 
    FROM Ticket
    JOIN Performance ON Ticket.PerformanceID = Performance.PerformanceID
    JOIN TheaterPlay ON Performance.PlayID = TheaterPlay.PlayID
    JOIN TheaterHalls ON Ticket.THID = TheaterHalls.THID
    JOIN Area ON Ticket.THID = Area.THID AND Ticket.AreaID = Area.AreaID
    JOIN Chair ON Area.THID = Chair.THID AND Area.AreaID = Chair.AreaID 
        AND Ticket.ChairNO = Chair.ChairNO AND Ticket.RowNO = Chair.RowNO
    WHERE TheaterPlay.Name = ? 
    AND Performance.Date = ? 
    AND Performance.Time = ? 
    AND TheaterHalls.Name = ? 
    AND Area.Name = ? 
    AND Chair.RowNO = ? 
    AND Chair.ChairNO = ?
    ) AS IsOccupied;
    """
    cur = conn.cursor()
    cur.execute(sql, (play, date, time, hall_name, area, row_no, seat_no))
    result = cur.fetchone()
    return result[0] == 1  # Returns True if occupied, False otherwise

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


def main_menu(conn):
    # connect to database
    cursor = conn.cursor()
    logged_off = False
    while not logged_off:
        print(
            """
            1. Initialize Database and Insert Initial Data
            2. Insert data
            3. Check Chair Availability
            4. Buy Tickets
            5. Find performances and ticket sales by date
            6. What actors are playing in a given play
            7. Most popular play
            8. Find co-actors for a given actor
            9. Exit
            """
        )

        choice = input("Enter your choice: ")


        if choice == '1':
            database.initialize_db()
            database.fill_db()
            clear_screen()

        elif choice == "2":
            # Insert data
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
            pass
        elif choice == "3":
            # Check Chair Availability
            # check_chair_availability(conn)
            # Read data from the text files
            pass

        elif choice == "4":
            # Buy 9 Tickets
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
            selected_date = None
            while selected_date is None:
                selected_date = prompt_user_for_date_from_df(date_times)

            results = get_performances_and_ticket_sales_by_date(conn, selected_date)
            if results:
                for play_name, date, tickets_sold in results:
                    print(
                        f"Play: {play_name}, Date: {date}, Tickets Sold: {tickets_sold}"
                    )
            else:
                print("No performances found for this date.")

        elif choice == "6":
            actors_and_roles = get_actors_and_roles(conn)
            for play, actor, role in actors_and_roles:
                print(f"{actor} is playing {role} in {play}")
        elif choice == "7":
            # 6. Most popular play
            print("fetching most popular play...")
            best_selling_performances = get_best_selling_performances(conn)
            print("Most popular play(s):", best_selling_performances)

            # Print the results
            for play_name, date, tickets_sold in best_selling_performances:
                print(f"Play: {play_name}, Date: {date}, Tickets Sold: {tickets_sold}")

        elif choice == "8":
            # 8. Find co-actors for a given actor for a given actor
            selected_actor = None

            while selected_actor is None:
                selected_actor, selected_actor_eid = prompt_user_for_actor(conn)
            print(f"Co-actors for {selected_actor}:")
            coactors = find_coactors_by_actor_eid(conn, selected_actor_eid)
            print(coactors)

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
    return results


def manage_theater_halls():

    print("Theater Hall Management")


def manage_plays():

    print("Play Management")


def manage_employees():

    print("Employee Management")
    
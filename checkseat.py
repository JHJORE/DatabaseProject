# Here you will buy 9 adult tickets for the performance of Størst av alt er kjærligheten on 3
# February, where there are 9 tickets available and where the seats are in the same row. The
# chairs do not have to be next to each other. We want to get a total of what it costs to buy
# these tickets, but you don't need to take the payment itself into account, we assume it
# happens on another system that you don't need to create. This function will be implemented
# in Python and SQL.

import sqlite3
import database as db
import CLI as interface
import crud as c


def check_row_availability(conn, amount, name, date, time):

    if name == "Størst av alt er kjærligheten":
        playid = 2
    else:
        playid = 1
    thid = c.get_theater_play_by_playid(conn, playid)[3]

    chairs = c.get_chair_by_thid(conn, thid)
    play = c.get_theater_play_by_playid(conn, playid)[2]
    hall_name = c.get_theater_hall_by_thid(conn, thid)[1]

    # Initialize a dictionary to count available seats per row
    available_seats_per_row = {}

    for chair in chairs:
        row_no = chair[2]
        area = chair[1]
        seat_no = chair[3]

        dic_key = (row_no, area)

        # Assume check_if_chair_occupied returns True if occupied, False if available
        if check_individual_seat_availability(
            conn, date, time, play, area, hall_name, row_no, seat_no
        ):
            if dic_key in available_seats_per_row:
                available_seats_per_row[dic_key] += 1
            else:
                available_seats_per_row[dic_key] = 1

    # Check if any row has the required number of available seats
    for (row_no, area), available_seats in available_seats_per_row.items():
        if available_seats >= amount:
            print(f"Row {row_no} in {area} has at least {amount} available seats.")
            return True

    print("No row has the required number of available seats.")
    return False


def check_individual_seat_availability(
    conn, date, time, play, areaname, thid, row_no, seat_no
):
    cur = conn.cursor()
    # Find PerformanceID
    performance = c.get_performance_by_date_and_playname(conn, date, play)
    if not performance:
        return False

    performance_id = performance[0]

    # Check if the seat is taken
    seat_query = """
    SELECT * FROM Ticket 
    JOIN Area ON Ticket.THID = Area.THID AND Ticket.Name = Area.Name
    WHERE PerformanceID=? AND Ticket.THID=? AND Ticket.Name=? AND RowNO=? AND ChairNO=?"""
    cur.execute(seat_query, (performance_id, thid, areaname, row_no, seat_no))
    seat = cur.fetchone()

    if seat:
        return False
    else:
        return True

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

def check_seat_availibity(conn, amount, name, date, time):
    
    if name == "Størst av alt er kjærligheten":
        playid = 1
    else:
        playid = 2
    thid = c.get_theater_play_by_playid(conn, playid)[3]
    
    chairs = c.get_chair_by_thid(conn, thid)
    play = c.get_theater_play_by_playid(conn, playid)[2]
    hall_name = c.get_theater_hall_by_thid(conn,thid)[1]
    
    
    # Initialize a dictionary to count available seats per row
    available_seats_per_row = {}
    
    for chair in chairs:
        row_no = chair[2]
        area = chair[1] 
        seat_no = chair[3]
        

        #Assume check_if_chair_occupied returns True if occupied, False if available
        if not interface.check_if_chair_occupied(conn, date, time, play, area, hall_name, row_no, seat_no):
            if row_no in available_seats_per_row:
                available_seats_per_row[row_no] += 1
            else:
                available_seats_per_row[row_no] = 1
    
    # Check if any row has the required number of available seats
    for row_no, available_seats in available_seats_per_row.items():
        if available_seats >= amount:
            print(f"Row {row_no} has at least {amount} available seats.")
            return True
    
    print("No row has the required number of available seats.")
    return False
 


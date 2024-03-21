import sqlite3

# Create -------------------------------------


def add_customer(conn, customer):
    sql = """ INSERT INTO CustomerProfile( MobileNo, Name, Address)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid


def add_order(conn, order):
    sql = """ INSERT INTO CustomerOrder( Time, Date, CID)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()
    return cur.lastrowid


def add_ticket(conn, ticket):
    sql = """ INSERT INTO Ticket( PerformanceID, SegmentID, OrderID, ChairNO, RowNO, Name, THID)
              VALUES(?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, ticket)
    conn.commit()
    return cur.lastrowid


def add_customer_group(conn, customer_group):
    sql = """ INSERT INTO CustomerGroup(SegmentID, Segment)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, customer_group)
    conn.commit()
    return cur.lastrowid


def add_performance(conn, performance):
    sql = """ INSERT INTO Performance( Date, Time, PlayID)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, performance)
    conn.commit()
    return cur.lastrowid


def add_has_group(conn, has_group):
    sql = """ INSERT INTO HasGroup(SegmentID, PlayID, Price)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, has_group)
    conn.commit()
    return (
        cur.lastrowid
    )  # Note: This return value might not be as meaningful due to the composite key


def add_theater_play(conn, theater_play):
    sql = """ INSERT INTO TheaterPlay( Season, Name, THID)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, theater_play)
    conn.commit()
    return cur.lastrowid


def add_assigned_backstage(conn, assigned_backstage):
    sql = """ INSERT INTO AssignedBackstage(EID, PlayID, Task)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, assigned_backstage)
    conn.commit()
    return cur.lastrowid


def add_employee(conn, employee):
    sql = """ INSERT INTO Employees(Name, Email, Phone, Status)
              VALUES(?,?, ?,?) """
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()
    return cur.lastrowid


def add_assigned_role(conn, assigned_role):
    sql = """ INSERT INTO AssignedRole(EID, RoleID)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, assigned_role)
    conn.commit()


def add_actor(conn, eid):
    sql = """ INSERT INTO Actor(EID) VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()


def add_manager(conn, eid):
    sql = """ INSERT INTO Manager(EID) VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()


def add_manager_of(conn, eid, playid):
    sql = """ INSERT INTO ManagerOf(EID, PlayID) VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, (eid, playid))
    conn.commit()


def add_backstage_employee(conn, eid):
    sql = """ INSERT INTO Backstage(EID) VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()


def add_role(conn, role):
    sql = """ INSERT INTO Role(Name) VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, role)
    conn.commit()


def add_role_in_act(conn, numid, roleid):
    sql = """ INSERT INTO RoleInAct(NumID, RoleID) VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, (numid, roleid))
    conn.commit()


def add_act(conn, act):
    sql = """ INSERT INTO Acts(Name) VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, act)
    conn.commit()


def add_part_of(conn, numid, playid):
    sql = """ INSERT INTO PartOf(NumID, PlayID) VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, (numid, playid))
    conn.commit()


def add_theater_hall(conn, theater_hall):
    sql = """ INSERT INTO TheaterHalls(Name, Capacity) VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, theater_hall)
    conn.commit()


def add_area(conn, area):
    sql = """ INSERT INTO Area(THID, AreaID, Name) VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, area)
    conn.commit()


def add_chair(conn, chair):
    sql = """ INSERT INTO Chair(THID, Name, ChairNo, RowNo) VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, chair)
    conn.commit()


# Read ---------------------------------------
def get_customer_by_cid(conn, cid):
    sql = """ SELECT * FROM CustomerProfile WHERE CID=? """
    cur = conn.cursor()
    cur.execute(sql, (cid,))
    return cur.fetchone()


def get_order_by_orderid(conn, orderid):
    sql = """ SELECT * FROM CustomerOrder WHERE OrderID=? """
    cur = conn.cursor()
    cur.execute(sql, (orderid,))
    return cur.fetchone()


def get_orders_by_customer(conn, cid):
    sql = """ SELECT * FROM CustomerOrder WHERE CID=? """
    cur = conn.cursor()
    cur.execute(sql, (cid,))
    return cur.fetchall()


def get_ticket_by_ticketid(conn, ticketid):
    sql = """ SELECT * FROM Ticket WHERE TicketID=? """
    cur = conn.cursor()
    cur.execute(sql, (ticketid,))
    return cur.fetchone()


def get_tickets_by_performanceid(conn, performanceid):
    sql = """ SELECT * FROM Ticket WHERE PerformanceID=? """
    cur = conn.cursor()
    cur.execute(sql, (performanceid,))
    return cur.fetchall()


def get_tickets_by_segmentid(conn, segmentid):
    sql = """ SELECT * FROM Ticket WHERE SegmentID=? """
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    return cur.fetchall()


def get_tickets_by_orderid(conn, orderid):
    sql = """ SELECT * FROM Ticket WHERE OrderID=? """
    cur = conn.cursor()
    cur.execute(sql, (orderid,))
    return cur.fetchall()


def get_tickets_by_thid(conn, thid):
    sql = """ SELECT * FROM Ticket WHERE THID=? """
    cur = conn.cursor()
    cur.execute(sql, (thid,))
    return cur.fetchall()


def get_customer_group_by_segmentid(conn, segmentid):
    sql = """ SELECT * FROM CustomerGroup WHERE SegmentID=? """
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    return cur.fetchone()


def get_performance_by_performanceid(conn, performanceid):
    sql = """ SELECT * FROM Performance WHERE PerformanceID=? """
    cur = conn.cursor()
    cur.execute(sql, (performanceid,))
    return cur.fetchone()


def get_performances_by_playid(conn, playid):
    sql = """ SELECT * FROM Performance WHERE PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (playid,))
    return cur.fetchall()


def get_has_group(conn, segment_id, play_id):
    sql = """ SELECT * FROM HasGroup WHERE SegmentID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (segment_id, play_id))
    return cur.fetchone()


def get_has_groups_for_segment(conn, segment_id):
    sql = """ SELECT * FROM HasGroup WHERE SegmentID=? """
    cur = conn.cursor()
    cur.execute(sql, (segment_id,))
    return cur.fetchall()


def get_has_groups_for_play(conn, play_id):
    sql = """ SELECT * FROM HasGroup WHERE PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (play_id,))
    return cur.fetchall()


def get_theater_play_by_playid(conn, playid):
    sql = """ SELECT * FROM TheaterPlay WHERE PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (playid,))
    return cur.fetchone()


def get_theater_plays_by_thid(conn, thid):
    sql = """ SELECT * FROM TheaterPlay WHERE THID=? """
    cur = conn.cursor()
    cur.execute(sql, (thid,))
    return cur.fetchall()


def get_assigned_backstage(conn, eid, playid):
    sql = """ SELECT * FROM AssignedBackstage WHERE EID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid, playid))
    return cur.fetchall()


def get_assignments_by_eid(conn, eid):
    sql = """ SELECT * FROM AssignedBackstage WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    return cur.fetchall()


def get_assignments_by_playid(conn, playid):
    sql = """ SELECT * FROM AssignedBackstage WHERE PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (playid,))
    return cur.fetchall()


def get_employee_by_eid(conn, eid):
    sql = """ SELECT * FROM Employees WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    return cur.fetchone()


def get_roles_by_eid(conn, eid):
    sql = """ SELECT * FROM AssignedRole WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    return cur.fetchall()


def get_employees_by_roleid(conn, roleid):
    sql = """ SELECT * FROM AssignedRole WHERE RoleID=? """
    cur = conn.cursor()
    cur.execute(sql, (roleid,))
    return cur.fetchall()


def get_all_actors(conn):
    sql = """ SELECT * FROM Actor """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def get_all_managers(conn):
    sql = """ SELECT * FROM Manager """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def get_plays_by_manager(conn, eid):
    sql = """ SELECT * FROM ManagerOf WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    return cur.fetchall()


def get_managers_of_play(conn, playid):
    sql = """ SELECT * FROM ManagerOf WHERE PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (playid,))
    return cur.fetchall()


def get_backstage_employee(conn, eid):
    sql = """ SELECT * FROM Backstage WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    return cur.fetchone()


def get_role_by_roleid(conn, roleid):
    sql = """ SELECT * FROM Role WHERE RoleID=? """
    cur = conn.cursor()
    cur.execute(sql, (roleid,))
    return cur.fetchone()


def get_roles_by_numid(conn, numid):
    sql = """ SELECT * FROM RoleInAct WHERE NumID=? """
    cur = conn.cursor()
    cur.execute(sql, (numid,))
    return cur.fetchall()


def get_actor_by_eid(conn, eid):
    sql = """ SELECT * FROM Actor WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    return cur.fetchone()


def get_acts_by_roleid(conn, roleid):
    sql = """ SELECT * FROM RoleInAct WHERE RoleID=? """
    cur = conn.cursor()
    cur.execute(sql, (roleid,))
    return cur.fetchall()


def get_act_by_numid(conn, numid):
    sql = """ SELECT * FROM Acts WHERE NumID=? """
    cur = conn.cursor()
    cur.execute(sql, (numid,))
    return cur.fetchone()


def get_acts_for_play(conn, playid):
    sql = """ SELECT Acts.* FROM Acts
              INNER JOIN PartOf ON Acts.NumID = PartOf.NumID
              WHERE PartOf.PlayID = ? """
    cur = conn.cursor()
    cur.execute(sql, (playid,))
    return cur.fetchall()


def get_plays_for_play_act(conn, numid):
    sql = """ SELECT TheaterPlay.* FROM TheaterPlay
              INNER JOIN PartOf ON TheaterPlay.PlayID = PartOf.PlayID
              WHERE PartOf.NumID = ? """
    cur = conn.cursor()
    cur.execute(sql, (numid,))
    return cur.fetchall()


def get_theater_hall_by_thid(conn, thid):
    sql = """ SELECT * FROM TheaterHalls WHERE THID=? """
    cur = conn.cursor()
    cur.execute(sql, (thid,))
    return cur.fetchone()


def get_area_by_name(conn, thid, name):
    sql = """ SELECT * FROM Area WHERE THID=? AND Name=? """
    cur = conn.cursor()
    cur.execute(sql, (thid, name))
    return cur.fetchone()


def get_areas_by_thid(conn, thid):
    sql = """ SELECT * FROM Area WHERE THID=? """
    cur = conn.cursor()
    cur.execute(sql, (thid,))
    return cur.fetchall()


def get_chair(conn, thid, name, chairno, rowno):
    sql = """ SELECT * FROM Chair WHERE THID=? AND Name=? AND ChairNo=? AND RowNo=? """
    cur = conn.cursor()
    cur.execute(sql, (thid, name, chairno, rowno))
    return cur.fetchone()


# Update -------------------------------------


def update_customer(conn, customer):
    sql = """ UPDATE CustomerProfile
              SET MobileNo=?, Name=?, Address=?
              WHERE CID=? """
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()


def update_order(conn, order):
    sql = """ UPDATE CustomerOrder
              SET Time=?, Date=?, CID=?
              WHERE OrderID=? """
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()


def update_ticket(conn, ticket):
    sql = """ UPDATE Ticket
              SET PerformanceID=?, SegmentID=?, OrderID=?, ChairNO=?, RowNO=?, Name=?, THID=?
              WHERE TicketID=? """
    cur = conn.cursor()
    cur.execute(sql, ticket)
    conn.commit()


def delete_customer_group(conn, segmentid):
    sql = """ DELETE FROM CustomerGroup WHERE SegmentID=? """
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    conn.commit()


def update_performance(conn, performance):
    sql = """ UPDATE Performance
              SET Date=?, Time=?, PlayID=?
              WHERE PerformanceID=? """
    cur = conn.cursor()
    cur.execute(sql, performance)
    conn.commit()


def update_has_group_price(conn, segment_id, play_id, new_price):
    sql = """ UPDATE HasGroup
              SET Price=?
              WHERE SegmentID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (new_price, segment_id, play_id))
    conn.commit()


def update_theater_play(conn, theater_play):
    sql = """ UPDATE TheaterPlay
              SET Season=?, Name=?, THID=?
              WHERE PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, theater_play)
    conn.commit()


def update_assigned_backstage_task(conn, eid, playid, new_task):
    sql = """ UPDATE AssignedBackstage
              SET Task=?
              WHERE EID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (new_task, eid, playid))
    conn.commit()


def update_employee(conn, employee):
    sql = """ UPDATE Employees
              SET Name=?, Email=?, Status=?
              WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()


# Hypothetical update, not applicable with the current schema attributes
def update_manager_of(conn, eid, playid, new_playid):
    sql = """ UPDATE ManagerOf SET PlayID=? WHERE EID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (new_playid, eid, playid))
    conn.commit()


def update_role(conn, role):
    sql = """ UPDATE Role SET Name=? WHERE RoleID=? """
    cur = conn.cursor()
    cur.execute(sql, role)
    conn.commit()


def update_act(conn, act):
    sql = """ UPDATE Acts SET Name=? WHERE NumID=? """
    cur = conn.cursor()
    cur.execute(sql, act)
    conn.commit()


def update_theater_hall(conn, theater_hall):
    sql = """ UPDATE TheaterHalls SET Name=?, Capacity=? WHERE THID=? """
    cur = conn.cursor()
    cur.execute(sql, theater_hall)
    conn.commit()


# Delete -------------------------------------


def delete_customer(conn, cid):
    sql = """ DELETE FROM CustomerProfile WHERE CID=? """
    cur = conn.cursor()
    cur.execute(sql, (cid,))
    conn.commit()


def delete_order(conn, orderid):
    sql = """ DELETE FROM CustomerOrder WHERE OrderID=? """
    cur = conn.cursor()
    cur.execute(sql, (orderid,))
    conn.commit()


def delete_ticket(conn, ticketid):
    sql = """ DELETE FROM Ticket WHERE TicketID=? """
    cur = conn.cursor()
    cur.execute(sql, (ticketid,))
    conn.commit()


def delete_customer_group(conn, segmentid):
    sql = """ DELETE FROM CustomerGroup WHERE SegmentID=? """
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    conn.commit()


def delete_performance(conn, performanceid):
    sql = """ DELETE FROM Performance WHERE PerformanceID=? """
    cur = conn.cursor()
    cur.execute(sql, (performanceid,))
    conn.commit()


def delete_has_group(conn, segment_id, play_id):
    sql = """ DELETE FROM HasGroup WHERE SegmentID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (segment_id, play_id))
    conn.commit()


def delete_theater_play(conn, playid):
    sql = """ DELETE FROM TheaterPlay WHERE PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (playid,))
    conn.commit()


def delete_assigned_backstage(conn, eid, playid):
    sql = """ DELETE FROM AssignedBackstage WHERE EID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid, playid))
    conn.commit()


def delete_employee(conn, eid):
    sql = """ DELETE FROM Employees WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()


def delete_assigned_role(conn, eid, roleid):
    sql = """ DELETE FROM AssignedRole WHERE EID=? AND RoleID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid, roleid))
    conn.commit()


def delete_actor(conn, eid):
    sql = """ DELETE FROM Actor WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()


def delete_manager(conn, eid):
    sql = """ DELETE FROM Manager WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()


def delete_manager_of(conn, eid, playid):
    sql = """ DELETE FROM ManagerOf WHERE EID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid, playid))
    conn.commit()


def delete_backstage_employee(conn, eid):
    sql = """ DELETE FROM Backstage WHERE EID=? """
    cur = conn.cursor()
    cur.execute(sql, (eid,))
    conn.commit()


def delete_role(conn, roleid):
    sql = """ DELETE FROM Role WHERE RoleID=? """
    cur = conn.cursor()
    cur.execute(sql, (roleid,))
    conn.commit()


def delete_role_in_act(conn, numid, roleid):
    sql = """ DELETE FROM RoleInAct WHERE NumID=? AND RoleID=? """
    cur = conn.cursor()
    cur.execute(sql, (numid, roleid))
    conn.commit()


def delete_act(conn, numid):
    sql = """ DELETE FROM Acts WHERE NumID=? """
    cur = conn.cursor()
    cur.execute(sql, (numid,))
    conn.commit()


def delete_part_of(conn, numid, playid):
    sql = """ DELETE FROM PartOf WHERE NumID=? AND PlayID=? """
    cur = conn.cursor()
    cur.execute(sql, (numid, playid))
    conn.commit()


def delete_theater_hall(conn, thid):
    sql = """ DELETE FROM TheaterHalls WHERE THID=? """
    cur = conn.cursor()
    cur.execute(sql, (thid,))
    conn.commit()


def delete_area(conn, thid, name):
    sql = """ DELETE FROM Area WHERE THID=? AND Name=? """
    cur = conn.cursor()
    cur.execute(sql, (thid, name))
    conn.commit()


def delete_chair(conn, thid, name, chairno, rowno):
    sql = """ DELETE FROM Chair WHERE THID=? AND Name=? AND ChairNo=? AND RowNo=? """
    cur = conn.cursor()
    cur.execute(sql, (thid, name, chairno, rowno))
    conn.commit()


# Other -------------------------------------


def print_all_tables(conn):
    # List of table names to query. Adjust as needed.
    tables = [
        "CustomerProfile",
        "Employees",
        "plays",
        "actors",
        "tickets",
        "theater_halls",
        "plays_actors",
        "employees_theater_halls",
        "employees_roles",
        "roles",
        "users",
    ]
    c = conn.cursor()

    for table in tables:
        print(f"\nContents of {table}:")
        try:
            c.execute(f"SELECT * FROM {table}")
            rows = c.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print(f"Error fetching data from {table}: {e}")

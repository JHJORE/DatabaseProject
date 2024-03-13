from database import connect_db

conn = connect_db()
cursor = conn.cursor()

#Create -------------------------------------

def add_customer(conn, customer):
    sql = ''' INSERT INTO CustomerProfile(CID, MobileNo, Name, Address)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid

def add_order(conn, order):
    sql = ''' INSERT INTO CustomerOrder(OrderID, Time, Date, CID)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()
    return cur.lastrowid

def add_ticket(conn, ticket):
    sql = ''' INSERT INTO Ticket(TicketID, PerformanceID, SegmentID, OrderID, ChairNO, RowNO, Name, THID)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, ticket)
    conn.commit()
    return cur.lastrowid

def add_customer_group(conn, customer_group):
    sql = ''' INSERT INTO CustomerGroup(SegmentID, Segment)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer_group)
    conn.commit()
    return cur.lastrowid

def add_performance(conn, performance):
    sql = ''' INSERT INTO Performance(PerformanceID, Date, Time, PlayID)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, performance)
    conn.commit()
    return cur.lastrowid




#Read ---------------------------------------
def get_customer_by_cid(conn, cid):
    sql = ''' SELECT * FROM CustomerProfile WHERE CID=? '''
    cur = conn.cursor()
    cur.execute(sql, (cid,))
    return cur.fetchone()

def get_order_by_orderid(conn, orderid):
    sql = ''' SELECT * FROM CustomerOrder WHERE OrderID=? '''
    cur = conn.cursor()
    cur.execute(sql, (orderid,))
    return cur.fetchone()

def get_orders_by_customer(conn, cid):
    sql = ''' SELECT * FROM CustomerOrder WHERE CID=? '''
    cur = conn.cursor()
    cur.execute(sql, (cid,))
    return cur.fetchall()

def get_ticket_by_ticketid(conn, ticketid):
    sql = ''' SELECT * FROM Ticket WHERE TicketID=? '''
    cur = conn.cursor()
    cur.execute(sql, (ticketid,))
    return cur.fetchone()

def get_tickets_by_performanceid(conn, performanceid):
    sql = ''' SELECT * FROM Ticket WHERE PerformanceID=? '''
    cur = conn.cursor()
    cur.execute(sql, (performanceid,))
    return cur.fetchall()

def get_tickets_by_segmentid(conn, segmentid):
    sql = ''' SELECT * FROM Ticket WHERE SegmentID=? '''
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    return cur.fetchall()

def get_tickets_by_orderid(conn, orderid):
    sql = ''' SELECT * FROM Ticket WHERE OrderID=? '''
    cur = conn.cursor()
    cur.execute(sql, (orderid,))
    return cur.fetchall()

def get_tickets_by_thid(conn, thid):
    sql = ''' SELECT * FROM Ticket WHERE THID=? '''
    cur = conn.cursor()
    cur.execute(sql, (thid,))
    return cur.fetchall()

def get_customer_group_by_segmentid(conn, segmentid):
    sql = ''' SELECT * FROM CustomerGroup WHERE SegmentID=? '''
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    return cur.fetchone()

def get_performance_by_performanceid(conn, performanceid):
    sql = ''' SELECT * FROM Performance WHERE PerformanceID=? '''
    cur = conn.cursor()
    cur.execute(sql, (performanceid,))
    return cur.fetchone()

def get_performances_by_playid(conn, playid):
    sql = ''' SELECT * FROM Performance WHERE PlayID=? '''
    cur = conn.cursor()
    cur.execute(sql, (playid,))
    return cur.fetchall()



#Update -------------------------------------

def update_customer(conn, customer):
    sql = ''' UPDATE CustomerProfile
              SET MobileNo=?, Name=?, Address=?
              WHERE CID=? '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()

def update_order(conn, order):
    sql = ''' UPDATE CustomerOrder
              SET Time=?, Date=?, CID=?
              WHERE OrderID=? '''
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()


def update_ticket(conn, ticket):
    sql = ''' UPDATE Ticket
              SET PerformanceID=?, SegmentID=?, OrderID=?, ChairNO=?, RowNO=?, Name=?, THID=?
              WHERE TicketID=? '''
    cur = conn.cursor()
    cur.execute(sql, ticket)
    conn.commit()

def delete_customer_group(conn, segmentid):
    sql = ''' DELETE FROM CustomerGroup WHERE SegmentID=? '''
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    conn.commit()

def update_performance(conn, performance):
    sql = ''' UPDATE Performance
              SET Date=?, Time=?, PlayID=?
              WHERE PerformanceID=? '''
    cur = conn.cursor()
    cur.execute(sql, performance)
    conn.commit()


#Delete -------------------------------------
    
def delete_customer(conn, cid):
    sql = ''' DELETE FROM CustomerProfile WHERE CID=? '''
    cur = conn.cursor()
    cur.execute(sql, (cid,))
    conn.commit()

def delete_order(conn, orderid):
    sql = ''' DELETE FROM CustomerOrder WHERE OrderID=? '''
    cur = conn.cursor()
    cur.execute(sql, (orderid,))
    conn.commit()

def delete_ticket(conn, ticketid):
    sql = ''' DELETE FROM Ticket WHERE TicketID=? '''
    cur = conn.cursor()
    cur.execute(sql, (ticketid,))
    conn.commit()

def delete_customer_group(conn, segmentid):
    sql = ''' DELETE FROM CustomerGroup WHERE SegmentID=? '''
    cur = conn.cursor()
    cur.execute(sql, (segmentid,))
    conn.commit()

def delete_performance(conn, performanceid):
    sql = ''' DELETE FROM Performance WHERE PerformanceID=? '''
    cur = conn.cursor()
    cur.execute(sql, (performanceid,))
    conn.commit()





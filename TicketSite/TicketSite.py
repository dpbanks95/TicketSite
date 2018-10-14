import psycopg2
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)

def getConn():
    #function to retrieve the password, construct
    #the connection string, make a connection and return it.
    pwFile = open("pw.txt", "r")
    pw = pwFile.read();
    pwFile.close()
    connStr = "host='cmpstudb-01.cmp.uea.ac.uk' \
               dbname= 'qxz14sru' user='qxz14sru' password = " + pw
    conn=psycopg2.connect(connStr)
    return conn

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')         

@app.route('/addCustomer', methods =['POST'])
def addCustomer():
    try:
        customerid = request.form['id']
        name = request.form['name']
        email = request.form['email']
        conn=None   
        conn=getConn()
        cur = conn.cursor()
        cur.execute('SET search_path to public')
        
        cur.execute('INSERT INTO Customer(CustomerID, Name, Email) \
        VALUES(%s, %s, %s)', [customerid, name, email])
        conn.commit()
        return render_template('index.html', msg1 = 'Customer Added')
    
    except Exception as e:
        return render_template('index.html', msg1 = 'Customer NOT Added', error1=e)
    finally:
        if conn:
            conn.close()
    
@app.route('/addTicket', methods =['POST'])
def addTicket():
    try:
        conn=None   
        conn=getConn()
        cur = conn.cursor()
        ticketID = request.form['ticketID']
        problem = request.form['problem']
        status = request.form['status']
        priority = request.form['priority']
        customerID = request.form['customerID']
        productID = request.form['productID']
        cur.execute('SET search_path to public')
        
        cur.execute('INSERT INTO Ticket(TicketID, Problem, Status, Priority, LoggedTime, CustomerID, ProductID) \
        VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)', [ticketID, problem, status, priority, customerID, productID])
        conn.commit()
        return render_template('index.html', msg2 = 'Ticket Sucessfully Added:', msg3 = 'TicketID: '+ticketID, msg4=' - Problem: '+problem, msg5=' - Status: '+status, msg6=' - Priority: '+priority, msg7=' - CustomerID: '+customerID, msg8=' - ProductID: '+productID)
    
    except Exception as e:
        return render_template('index.html', msg2 = 'Ticket NOT Added', error2=e)
    
    finally:
        if conn:
            conn.close()

@app.route('/updateTicket', methods =['POST'])
def updateTicket():
    try:
        conn=None   
        conn=getConn()
        cur = conn.cursor()
        updateID = request.form['id']
        message = request.form['message']
        ticketID = request.form['ticketID']
        staffID = request.form['staffID']
        cur.execute('SET search_path to public')
        
        if staffID == '':
            staffID = None
        
        cur.execute('INSERT INTO TicketUpdate(TicketUpdateID, Message, UpdateTime, TicketID, StaffID) \
        VALUES(%s, %s, CURRENT_TIMESTAMP, %s, %s)', [updateID, message, ticketID, staffID])
        conn.commit()
        return render_template('index.html', ticketUpdate = 'Update Added')
    
    except Exception as e:
        return render_template('index.html', ticketUpdate = 'Customer NOT Added', error3=e)
    finally:
        if conn:
            conn.close()

@app.route('/closeTicket', methods =['POST'])
def closeTicket():
    try:
        conn=None   
        conn=getConn()
        cur = conn.cursor()
        ticketID = request.form['ticketID']
        cur.execute('SET search_path to public')
        
        cur.execute("UPDATE Ticket SET Status='closed' WHERE TicketID=%s", [ticketID])
        conn.commit()
        return render_template('index.html', closeTicket = 'Ticket closed')
    
    except Exception as e:
        return render_template('index.html', closeTicket = 'Ticket NOT closed', error4=e)
    finally:
        if conn:
            conn.close()

@app.route('/openTickets', methods =['GET'])
def openTickets():
    try:
        conn=None   
        conn=getConn()
        cur = conn.cursor()
        cur.execute('SET search_path to public')
        
        cur.execute("SELECT t.TicketID, t.status, t.LoggedTime, MAX(tu.UpdateTime) FROM Ticket t LEFT JOIN TicketUpdate tu ON t.TicketID = tu.TicketID WHERE Status='open' GROUP BY t.TicketID ORDER BY t.LoggedTime")
        conn.commit()
        
        rows = cur.fetchall()
        if rows:
            return render_template('openTickets.html', rows = rows)
        else:
            return render_template('index.html', openTickets = 'No data found')
    
    except Exception as e:
        return render_template('index.html', openTickets = 'Error', error5=e)
    finally:
        if conn:
            conn.close()

@app.route('/getTicket', methods =['GET'])
def getTicket():
    try:
        conn=None
        conn=getConn()
        cur = conn.cursor()
        ticketID = request.args['ticketID']
        cur.execute('SET search_path to public')
        
        cur.execute("SELECT Ticket.TicketID, Ticket.Problem, TicketUpdate.Message, TicketUpdate.UpdateTime, coalesce(Staff.Name, Customer.Name) \
        FROM Ticket LEFT JOIN TicketUpdate ON Ticket.TicketID = TicketUpdate.TicketID LEFT JOIN Staff ON TicketUpdate.StaffID = Staff.StaffID LEFT JOIN Customer ON Ticket.CustomerID = Customer.CustomerID \
        WHERE Ticket.TicketID = %s ORDER BY TicketUpdate.UpdateTime", [ticketID])
        conn.commit()
        
        rows = cur.fetchall()
        if rows:
            return render_template('getTicket.html', rows = rows, ticketID=ticketID)
        else:
            return render_template('index.html', getTicket = 'No data found')
    
    except Exception as e:
        return render_template('index.html', getTicket = 'Error', error6=e)
    finally:
        if conn:
            conn.close()

@app.route('/closedTickets', methods =['GET'])
def closedTickets():
    try:
        conn=None   
        conn=getConn()
        cur = conn.cursor()
        cur.execute('SET search_path to public')
        
        cur.execute("SELECT t.TicketID, t.Problem, COUNT(tu.UpdateTime), MIN(tu.UpdateTime) - t.LoggedTime, MAX(tu.UpdateTime) - t.LoggedTime \
        FROM Ticket t LEFT JOIN TicketUpdate tu ON t.TicketID = tu.TicketID \
        WHERE t.Status ='closed' GROUP BY t.TicketID")
        conn.commit()
        
        rows = cur.fetchall()
        if rows:
            return render_template('closedTickets.html', rows = rows)
        else:
            return render_template('index.html', closedTickets = 'No data found')
    
    except Exception as e:
        return render_template('index.html', closedTickets = 'Error', error7=e)
    finally:
        if conn:
            conn.close()

@app.route('/closeOldTickets', methods =['GET'])
def closeOldTickets():
    try:
        conn=None
        conn=getConn()
        cur = conn.cursor()
        cur.execute('SET search_path to public')
        numTickets=()
        cur.execute("UPDATE Ticket SET Status = 'closed' \
        FROM(SELECT t.* FROM Ticket t LEFT JOIN TicketUpdate tu ON t.TicketID = tu.TicketID \
            WHERE  tu.StaffID IS NOT NULL AND t.status = 'open' AND tu.UpdateTime <= NOW() - interval '1 day') AS subquery \
        WHERE Ticket.Ticketid = subquery.Ticketid")
        numrows = cur.rowcount
        
        if numrows == 0:
            conn.commit()
            return render_template('index.html', closeOldTickets = 'No Tickets to close')
        else:
            conn.commit()
            return render_template('index.html', closeOldTickets = str(numrows)+' Old Ticket(s) closed')
    
    except Exception as e:
        return render_template('index.html', closeOldTickets = 'Old Tickets NOT closed', error8=e)
    finally:
        if conn:
            conn.close()

@app.route('/deleteCustomer', methods =['POST'])
def deleteCustomer():
    try:
        conn=None
        conn=getConn()
        cur = conn.cursor()
        customerID = request.form['customerID']
        cur.execute('SET search_path to public')
        
        cur.execute("DELETE FROM Customer AS c WHERE c.CustomerID =%s AND %s NOT IN (SELECT CustomerID FROM Ticket)", [customerID, customerID])
        
        numrows = cur.rowcount
        
        if numrows == 0:
            return render_template('index.html', deleteCustomer = 'Customer either does not exist or is associasted with a ticket')
        else:
            conn.commit()
            return render_template('index.html', deleteCustomer = 'Customer Deleted')
    
    except Exception as e:
        return render_template('index.html', deleteCustomer = 'Customer NOT Deleted', error9=e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug = True)
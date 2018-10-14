CREATE TABLE Staff(
	StaffID	INTEGER PRIMARY KEY,
	Name	VARCHAR(40) NOT NULL
	)

CREATE TABLE Product(
	ProductID	INTEGER PRIMARY KEY,
	Name	VARCHAR(40) NOT NULL
	)

CREATE TABLE Customer(	
	CustomerID	INTEGER PRIMARY KEY,
	Name	VARCHAR(40) NOT NULL,
	Email	VARCHAR(40) NOT NULL
	)

CREATE TABLE Ticket(	
	TicketID	INTEGER PRIMARY KEY,
	Problem	VARCHAR(1000) NOT NULL,
	Status	VARCHAR(20) NOT NULL DEFAULT 'open' CONSTRAINT statusCheck
		CHECK (Status IN('open','closed')),
	Priority INTEGER NOT NULL DEFAULT 1 CONSTRAINT priorityCheck
		CHECK (Priority IN(1, 2, 3)),
	LoggedTime TIMESTAMP NOT NULL,
	CustomerID INTEGER NOT NULL,
	ProductID INTEGER NOT NULL,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) 
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
		ON DELETE CASCADE ON UPDATE CASCADE
	)
	
CREATE TABLE TicketUpdate(
	TicketUpdateID	INTEGER PRIMARY KEY,
	Message	VARCHAR(1000) NOT NULL,
	UpdateTime TIMESTAMP NOT NULL,
	TicketID INTEGER NOT NULL,
	StaffID	INTEGER DEFAULT NULL,
	FOREIGN KEY (TicketID) REFERENCES Ticket(TicketID)
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
		ON DELETE CASCADE ON UPDATE CASCADE
	)

--1
INSERT INTO Customer(CustomerID, Name, Email)
VALUES(1,'Delete','as@as.as')
--

--2
INSERT INTO Ticket(TicketID, Problem, Status, Priority, LoggedTime, CustomerID, ProductID)
VALUES(2, 'Test open', 'open', 2, CURRENT_TIMESTAMP, 1, 1)

SELECT * FROM TICKET
--

--3
INSERT INTO TicketUpdate(TicketUpdateID, Message, UpdateTime, TicketID, StaffID)
VALUES(1, 'test', CURRENT_TIMESTAMP, 1, null)
--

--4
SELECT t.TicketID AS Ticket_ID, t.status, t.LoggedTime, MAX(tu.UpdateTime)
FROM Ticket t LEFT JOIN TicketUpdate tu ON t.TicketID = tu.TicketID 
WHERE Status='open' GROUP BY Ticket_ID ORDER BY t.LoggedTime
--

--5
UPDATE Ticket SET Status='open' WHERE TicketID=1
--

--6
SELECT Ticket.TicketID, Ticket.Problem, TicketUpdate.Message, TicketUpdate.UpdateTime, coalesce(Staff.Name, Customer.Name)
FROM Ticket LEFT JOIN TicketUpdate ON Ticket.TicketID = TicketUpdate.TicketID LEFT JOIN Staff ON TicketUpdate.StaffID = Staff.StaffID LEFT JOIN Customer ON Ticket.CustomerID = Customer.CustomerID
WHERE Ticket.TicketID = 1
ORDER BY TicketUpdate.UpdateTime
--

--7
SELECT t.TicketID, t.Problem, COUNT(tu.UpdateTime), MIN(tu.UpdateTime) - t.LoggedTime, MAX(tu.UpdateTime) - t.LoggedTime
FROM Ticket t LEFT JOIN TicketUpdate tu ON t.TicketID = tu.TicketID
WHERE t.Status ='closed'
GROUP BY t.TicketID
--

--8
Begin
UPDATE Ticket
SET Status = 'closed'
FROM(
	SELECT t.TicketID, t.status, tu.UpdateTime, tu.StaffID
	FROM Ticket t LEFT JOIN TicketUpdate tu ON t.TicketID = tu.TicketID 
	WHERE  tu.StaffID IS NOT NULL AND t.status = 'open' AND tu.UpdateTime <= NOW() - interval '1 day'
	) AS subquery
WHERE Ticket.TicketID = subquery.TicketID

Rollback
Commit
--

--9
Begin
DELETE FROM Customer AS c
WHERE c.CustomerID = 69 AND 69 NOT IN (SELECT CustomerID FROM Ticket)

Rollback
Commit
--

-- Test Data
INSERT INTO Staff(StaffID, Name)
VALUES(1, 'Dan')
INSERT INTO Staff(StaffID, Name)
VALUES(2, 'John')
INSERT INTO Staff(StaffID, Name)
VALUES(3, 'Dave')
INSERT INTO Staff(StaffID, Name)
VALUES(4, 'Jane')

INSERT INTO Product(ProductID,Name)
VALUES(1,'spanner')
INSERT INTO Product(ProductID,Name)
VALUES(2,'computer')
INSERT INTO Product(ProductID,Name)
VALUES(3,'screwdriver')
INSERT INTO Product(ProductID,Name)
VALUES(4,'Laptep')

INSERT INTO Customer(CustomerID, Name, Email)
VALUES(1,'James','james@as.com')
INSERT INTO Customer(CustomerID, Name, Email)
VALUES(2,'Kyle','kyle@as.com')
INSERT INTO Customer(CustomerID, Name, Email)
VALUES(3,'Danny','danny@as.com')
INSERT INTO Customer(CustomerID, Name, Email)
VALUES(4,'Sarah','sarah@as.com')

INSERT INTO Ticket(TicketID, Problem, Status, Priority, LoggedTime, CustomerID, ProductID)
VALUES(1, 'customerid 1', 'open', 1, CURRENT_TIMESTAMP, 1, 1)
INSERT INTO Ticket(TicketID, Problem, Status, Priority, LoggedTime, CustomerID, ProductID)
VALUES(2, 'customerid 2', 'open', 2, CURRENT_TIMESTAMP, 2, 2)
INSERT INTO Ticket(TicketID, Problem, Status, Priority, LoggedTime, CustomerID, ProductID)
VALUES(3, 'customerid 3', 'open', 3, CURRENT_TIMESTAMP, 3, 3)
INSERT INTO Ticket(TicketID, Problem, Status, Priority, LoggedTime, CustomerID, ProductID)
VALUES(4, 'customerid 4', 'open', 3, CURRENT_TIMESTAMP, 4, 4)

INSERT INTO TicketUpdate(TicketUpdateID, Message, UpdateTime, TicketID, StaffID)
VALUES(1, 'customer update', CURRENT_TIMESTAMP, 1, null)
INSERT INTO TicketUpdate(TicketUpdateID, Message, UpdateTime, TicketID, StaffID)
VALUES(2, 'staff update', CURRENT_TIMESTAMP, 2, 1)
INSERT INTO TicketUpdate(TicketUpdateID, Message, UpdateTime, TicketID, StaffID)
VALUES(3, 'test update', CURRENT_TIMESTAMP, 3, 2)
INSERT INTO TicketUpdate(TicketUpdateID, Message, UpdateTime, TicketID, StaffID)
VALUES(4, 'test update 2', CURRENT_TIMESTAMP, 3, 2)





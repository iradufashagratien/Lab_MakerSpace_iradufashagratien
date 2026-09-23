import sqlite3

# The name of the database file with constant variable

DB_NAME = "makerspace.db"

def get_connection():

    # This function creates and opens the database file and gives us the connection.
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support    
    return connection

def create_tables(connection):

    #This function creates the tables in the database if they do not already exist.
    # The "IF NOT EXISTS" clause is used to avoid errors if the tables already exist.

    connection.execute("""

        CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL) 
    
    """)

    connection.execute("""

        CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        is_available INTEGER NOT NULL DEFAULT 1)
     
    """)

    connection.execute("""
        
        CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        equipment_id INTEGER NOT NULL,
        checkout_date TEXT,
        due_date TEXT,
        return_date TEXT, 
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
        FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
        )
    """)
    connection.execute("""
        CREATE TRIGGER IF NOT EXISTS mark_equipment_available_after_loan_delete
        AFTER DELETE ON loans
        BEGIN
            UPDATE equipment
            SET is_available = 1
            WHERE id = OLD.equipment_id;
        END;
    """)
    # Commit() the changes to the database to make sure the tables are created.
    connection.commit()


# ============== MEMBER FUNCTIONS ==============

 # This function adds a new member to the members table in the database.

def add_member(connection, name, email):

   
    # It takes the connection, name, and email as parameters.

    connection.execute(
        
        "INSERT INTO members (name, email) VALUES (?, ?)",
        (name, email)
    )
    connection.commit()


def get_all_members(connection):

    # fetchall() returns every record from the members table as a list.

    result  = connection.execute("SELECT * FROM members")
    return result.fetchall()

def get_member_by_id(connection, member_id):
    
    # This function retrieves a member's information from the members table based on their ID.

    result = connection.execute(
        "SELECT * FROM members WHERE id = ?",
        (member_id,)
    )

    #Fetchone() returns a single record from the members table as a tuple. If no record is found, it returns None.
    return result.fetchone()


  #This function updates a member's information in the members table based on their ID.

def update_member(connection, member_id, name, email):

    connection.execute(
        "UPDATE members SET name = ?, email = ? WHERE id = ?",
        (name, email, member_id)
    )
    connection.commit()


#Function to delete a member from the members table based on their ID.
# Because loans reference members with ON DELETE CASCADE,
# any loan records linked to that member are deleted automatically.

def delete_member(connection, member_id):
    connection.execute(
        "DELETE FROM members WHERE id = ?",
        (member_id,)
    )
    connection.commit() 

#The function searches for members in the members table based on a keyword in their name.
def search_members_by_name(connection, keyword):

    # The % signs mean "anything can come before or after the keyword"
    result = connection.execute(
        "SELECT * FROM members WHERE name LIKE ?",
        ("%" + keyword + "%",)
    )
    return result.fetchall()

#============= EQUIPMENT FUNCTIONS ============== 

def add_equipment(connection, name, category):

    # New equipment always starts as available (1 = True, 0 = False)

    connection.execute(
        "INSERT INTO equipment (name, category, is_available) VALUES (?, ?, 1)",
        (name, category)
    )
    connection.commit()


def get_all_equipment(connection):
    result = connection.execute("SELECT * FROM equipment")
    return result.fetchall()


def get_equipment_by_id(connection, equipment_id):
    result = connection.execute(
        "SELECT * FROM equipment WHERE id = ?",
        (equipment_id,)
    )
    return result.fetchone()


def update_equipment(connection, equipment_id, name, category):
    connection.execute(
        "UPDATE equipment SET name = ?, category = ? WHERE id = ?",
        (name, category, equipment_id)
    )
    connection.commit()


def delete_equipment(connection, equipment_id):
    connection.execute(
        "DELETE FROM equipment WHERE id = ?",
        (equipment_id,)
    )
    connection.commit()


def set_equipment_available(connection, equipment_id, available):
    # available should be True or False. We store it as 1 or 0.
    value = 1 if available else 0
    connection.execute(
        "UPDATE equipment SET is_available = ? WHERE id = ?",
        (value, equipment_id)
    )
    connection.commit()


def search_equipment_by_name(connection, keyword):
    result = connection.execute(
        "SELECT * FROM equipment WHERE name LIKE ?",
        ("%" + keyword + "%",)
    )
    return result.fetchall()

#============= LOAN FUNCTIONS ============== 

def add_loan(connection, member_id, equipment_id, checkout_date, due_date):
    connection.execute(
        """INSERT INTO loans (member_id, equipment_id, checkout_date, due_date, return_date)
           VALUES (?, ?, ?, ?, NULL)""",
        (member_id, equipment_id, checkout_date, due_date)
    )
    connection.commit()


def get_loan_by_id(connection, loan_id):
    result = connection.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    )
    return result.fetchone()


def close_loan(connection, loan_id, return_date):
    connection.execute(
        "UPDATE loans SET return_date = ? WHERE id = ?",
        (return_date, loan_id)
    )
    connection.commit()

# ======= REPORT FUNCTIONS =======

def report_active_loans(connection):
    # "Active" means return_date is still empty (NULL) = still borrowed
    result = connection.execute("""
        SELECT loans.id, members.name, equipment.name, loans.due_date
        FROM loans
        JOIN members ON loans.member_id = members.id
        JOIN equipment ON loans.equipment_id = equipment.id
        WHERE loans.return_date IS NULL
    """)
    return result.fetchall()

def report_overdue_loans(connection, today_date):
    result = connection.execute("""
        SELECT loans.id, members.name, equipment.name, loans.due_date
        FROM loans
        JOIN members ON loans.member_id = members.id
        JOIN equipment ON loans.equipment_id = equipment.id
        WHERE loans.return_date IS NULL AND loans.due_date < ?
    """, (today_date,))
    return result.fetchall()
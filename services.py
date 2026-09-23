# This file holds the "business rules" — the decisions about whether
# an action is allowed. main.py just asks a question (checkout? return?)
# and this file decides yes/no and does the work, then hands back a message.

from datetime import date, timedelta
import database
import models


def checkout(connection, member_id, equipment_id):
    # Returns a text message explaining what happened.
    # main.py will just print whatever this function returns.

    member_row = database.get_member_by_id(connection, member_id)
    if member_row is None:
        print()
        return "That member does not exist."

    equipment_row = database.get_equipment_by_id(connection, equipment_id)

    if equipment_row is None:
        print()
        return "That equipment does not exist."

    # Turn the row into an Equipment object so we can use is_available easily

    equipment = models.Equipment(equipment_row[0], equipment_row[1], equipment_row[2], equipment_row[3])

    if not equipment.is_available:
        print()
        return "Sorry, that equipment is already on loan."

    today = date.today()
    checkout_date = today.isoformat()
    due_date = (today + timedelta(days=7)).isoformat()  # due in 7 days

    database.add_loan(connection, member_id, equipment_id, checkout_date, due_date)
    database.set_equipment_available(connection, equipment_id, False)
    print()

    return f"Checked out! Due date is on {due_date}."


def return_item(connection, loan_id):
    loan_row = database.get_loan_by_id(connection, loan_id)
    if loan_row is None:
        print() 
        return "No loan found with that ID."

    # Turn the row into a Loan object so we can use is_returned() easily
    loan = models.Loan(loan_row[0], loan_row[1], loan_row[2], loan_row[3], loan_row[4], loan_row[5])
    if loan.is_returned():
        print()
        return "This loan was already returned."

    return_date = date.today().isoformat()
    database.close_loan(connection, loan_id, return_date)
    database.set_equipment_available(connection, loan.equipment_id, True)
    print()
    return "Equipment returned. Thank you!"
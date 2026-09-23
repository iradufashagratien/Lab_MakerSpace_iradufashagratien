import database
import models
import services
import validation
from datetime import date



# ======================================= MEMBER MANAGEMENT ===============================

def register_member(connection):
    name = validation.get_valid_name("Enter member name: ")
    email = validation.get_valid_email("Enter member email: ")
    database.add_member(connection, name, email)
    print()
    print("Member registered!")


def list_members(connection):
    rows = database.get_all_members(connection)
    if len(rows) == 0:
        print()
        print("No members yet!. Please make sure to register a member first.")
        return
    print("This is the list of all members in the database and their email addresses:")
    for row in rows:
        # Each row looks like (id, name, email). We turn it into a Member object.
        member = models.Member(row[0], row[1], row[2])
        print(member.display())



def update_member(connection):
    member_id = validation.get_valid_id("Enter member ID to update: ")

    existing = database.get_member_by_id(connection, member_id)
    if existing is None:
        print()
        print("No member found with that ID.")
        return

    new_name = validation.get_valid_name("Enter new name: ")
    new_email = validation.get_valid_email("Enter new email: ")
    database.update_member(connection, member_id, new_name, new_email)
    print()
    print("Member updated!")


def delete_member(connection):
    member_id = validation.get_valid_id("Enter member ID to delete: ")

    existing = database.get_member_by_id(connection, member_id)
    if existing is None:
        print()
        print("No member found with that ID.")
        return

    database.delete_member(connection, member_id)
    print()
    print("Member deleted.")


def search_member(connection):
    print("Search: 1) By name  2) By ID")
    choice = input("Choose: ")

    if choice == "1":
        keyword = validation.get_valid_text("Enter name to search: ", "Invalid name. Please enter letters only.")
        rows = database.search_members_by_name(connection, keyword)
        if len(rows) == 0:
            print()
            print("No matching members found.")
        for row in rows:
            member = models.Member(row[0], row[1], row[2])
            print(member.display())

    elif choice == "2":
        member_id = validation.get_valid_id("Enter member ID: ")
        row = database.get_member_by_id(connection, member_id)
        if row is None:
            print()
            print("No member found with that ID.")
        else:
            member = models.Member(row[0], row[1], row[2])
            print()
            print(member.display())

    else:
        print()
        print("Invalid choice.")


def member_menu(connection):
    while True:
        print("\n===================== MEMBER MANAGEMENT =====================")
        print()
        print("1. Register member")
        print("2. List members")
        print("3. Update member")
        print("4. Delete member")
        print("5. Search member")
        print("0. Back to main menu")
        print() 
        choice = input("Choose an option: ")
        print()


        if choice == "1":
            register_member(connection)
        elif choice == "2":
            list_members(connection)
        elif choice == "3":
            update_member(connection)
        elif choice == "4":
            delete_member(connection)
        elif choice == "5":
            search_member(connection)
        elif choice == "0":
            break
        else:
            print()
            print("Invalid option, please try again.")
            print()



# =========================== EQUIPMENT MANAGEMENT =================================

def register_equipment(connection):
    name = validation.get_valid_text("Enter equipment name: ", "Invalid equipment name. Please enter letters only.")
    category = validation.get_valid_text("Enter category: ", "Invalid category. Please enter letters only.")
    database.add_equipment(connection, name, category)
    print()
    print("Equipment registered!")


def list_equipment(connection):
    rows = database.get_all_equipment(connection)
    if len(rows) == 0:
        print()
        print("No equipment yet. Please make sure to register equipment first.")
        return

    print("This is the list of all equipment in the database and their availability status:")
    for row in rows:
        # Each row looks like (id, name, category, is_available)
        item = models.Equipment(row[0], row[1], row[2], row[3])
        print(item.display())

def update_equipment(connection):
    equipment_id = validation.get_valid_id("Enter equipment ID to update: ")

    existing = database.get_equipment_by_id(connection, equipment_id)
    if existing is None:
        print()
        print("No equipment found with that ID.")
        return

    new_name = validation.get_valid_text("Enter new name: ", "Invalid equipment name. Please enter letters only.")
    new_category = validation.get_valid_text("Enter new category: ", "Invalid category. Please enter letters only.")
    database.update_equipment(connection, equipment_id, new_name, new_category)
    print()
    print("Equipment updated!")


def delete_equipment(connection):
    equipment_id = validation.get_valid_id("Enter equipment ID to delete: ")

    existing = database.get_equipment_by_id(connection, equipment_id)
    if existing is None:
        print()
        print("No equipment found with that ID.")
        return

    database.delete_equipment(connection, equipment_id)
    print()
    print("Equipment deleted.")


def search_equipment(connection):
    print("Search: 1) By name  2) By ID")
    choice = input("Choose: ")

    if choice == "1":
        keyword = validation.get_valid_text("Enter equipment name to search: ", "Invalid equipment name. Please enter letters only.")
        rows = database.search_equipment_by_name(connection, keyword)
        if len(rows) == 0:
            print()
            print("No matching equipment found.")
        for row in rows:
            item = models.Equipment(row[0], row[1], row[2], row[3])
            print()
            print(item.display())

    elif choice == "2":
        equipment_id = validation.get_valid_id("Enter equipment ID: ")
        row = database.get_equipment_by_id(connection, equipment_id)
        if row is None:
            print()
            print("No equipment found with that ID.")
        else:
            item = models.Equipment(row[0], row[1], row[2], row[3])
            print()
            print(item.display())

    else:
        print()
        print("Invalid choice.")


def equipment_menu(connection):
    while True:
        print("\n===================== EQUIPMENT MANAGEMENT =====================")
        print()
        print("1. Register equipment")
        print("2. List equipment")
        print("3. Update equipment")
        print("4. Delete equipment")
        print("5. Search equipment")
        print("0. Back to main menu")
        print()

        choice = input("Choose an option: ")

        if choice == "1":
            register_equipment(connection)
        elif choice == "2":
            list_equipment(connection)
        elif choice == "3":
            update_equipment(connection)
        elif choice == "4":
            delete_equipment(connection)
        elif choice == "5":
            search_equipment(connection)
        elif choice == "0":
            break
        else:
            print()
            print("Invalid option, please try again.")


#  ======================= LOAN MANAGEMENT =====================================
# (This part now calls services.py instead of doing the checking itself)

def checkout_equipment(connection):
    member_id = validation.get_valid_id("Enter member ID: ")
    equipment_id = validation.get_valid_id("Enter equipment ID: ")

    # services.checkout() does all the checking and the database work,
    # and just hands us back a message to show the user.
    message = services.checkout(connection, member_id, equipment_id)
    print()
    print(message)


def return_equipment(connection):
    loan_id = validation.get_valid_id("Enter loan ID to return: ")

    message = services.return_item(connection, loan_id)
    print(message)


def loan_menu(connection):
    while True:
        print("\n===================== LOAN MANAGEMENT =====================")
        print()
        print("1. Checkout equipment (create a loan)")
        print("2. Return equipment")
        print("0. Back to main menu")
        print()

        choice = input("Choose an option: ")

        if choice == "1":
            checkout_equipment(connection)
        elif choice == "2":
            return_equipment(connection)
        elif choice == "0":
            break
        else:
            print()
            print("Invalid option, please try again.")



# ========================================== REPORTS ==========================================

def reports_menu(connection):
    while True:
        print("\n===================== REPORTS =====================")
        print()
        print("1. Currently borrowed items")
        print("2. Overdue loans")
        print("0. Back to main menu")
        print()
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            rows = database.report_active_loans(connection)
            if len(rows) == 0:
                print()
                print("Nothing is currently borrowed.")
            for row in rows:
                # row looks like (loan_id, member_name, equipment_name, due_date)
                print()
                print(f"Loan #{row[0]}: {row[1]} has {row[2]}, due {row[3]}")

        elif choice == "2":
            today_text = date.today().isoformat()
            rows = database.report_overdue_loans(connection, today_text)
            if len(rows) == 0:
                print()
                print("No overdue loans.")
            for row in rows:
                print()
                print(f"Loan #{row[0]}: {row[1]}'s {row[2]} was due {row[3]}")

        elif choice == "0":
            break
        else:
            print()
            print("Invalid option, please try again.")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    connection = database.get_connection()
    database.create_tables(connection)

    while True:
        print("\n===================== CAMPUS MAKERSPACE CHECKOUT SYSTEM =====================")
        print()
        print("1. Member Management")
        print("2. Equipment Management")
        print("3. Loan Management")
        print("4. Reports")
        print("0. Exit")
        print()


        choice = input("Choose an option: ")

        if choice == "1":
            member_menu(connection)
        elif choice == "2":
            equipment_menu(connection)
        elif choice == "3":
            loan_menu(connection)
        elif choice == "4":
            reports_menu(connection)
        elif choice == "0":
            print()
            print("Exiting the program...")
            print("Bye, See you next time!")
            print()
            break
        else:
            print()
            print("Invalid option, please try again.")
            print()

    connection.close()


if __name__ == "__main__":
    main()
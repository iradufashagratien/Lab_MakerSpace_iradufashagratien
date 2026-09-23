from datetime import date

class Member:
    # A member just stores its own data.

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    def display(self):
        return f"[{self.id}] {self.name} - {self.email}"
    

class Equipment:    

    def __init__(self, id, name, category, is_available):
        self.id = id
        self.name = name
        self.category = category

    # SQLite gives us 1 or 0, we turn it into True/False here

        self.is_available = bool(is_available)


    def display(self):
        status = "Available" if self.is_available else "On Loan"
        return f"[{self.id}] {self.name} ({self.category}) - {status}"

    
class Loan:

    def __init__(self, id, member_id, equipment_id, checkout_date, due_date, return_date):

        self.id = id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = return_date

    def is_returned(self):
        # If return_date has a value, it means it was already returned
        return self.return_date is not None

    def is_overdue(self):
        # Only check overdue if it's still out
        if self.is_returned():
            return False
        today_text = date.today().isoformat()
        return self.due_date < today_text

    def display(self):
        if self.is_returned():
            status = "Returned"
        elif self.is_overdue():
            status = "OVERDUE"
        else:
            status = "Active"
        print()    
        return f"Loan NO: {self.id} - Due to: {self.due_date} - {status}"
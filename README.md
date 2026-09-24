An individual Object-Oriented Python CLI application, backed by SQLite,
built for the "Introduction to Programming and Databases" summative
assessment. It lets a makerspace operator manage members, equipment,
and loans through a menu-driven interface, with all data persisted in
a local SQLite database file between runs.

## What This System Does

Members can borrow equipment (3D-printer accessories, soldering kits,
cameras, laptops, etc.) from a campus makerspace. This application lets
an operator:

- Register, list, update, delete, and search members
- Register, list, update, delete, and search equipment (with live
  availability status)
- Check out equipment to a member, with validation (member must exist,
  equipment must exist and be available)
- Return equipment, which automatically updates its availability
- Run reports on currently borrowed items and overdue loans
- Get clear error messages instead of crashes on invalid input

## Requirements

- Python 3 (no third-party packages needed - `sqlite3` and `datetime`
  are both part of the Python standard library)
- No installation steps beyond having Python 3 available; there is no
  `requirements.txt` because nothing outside the standard library is
  used

## Project Structure

| File            | Responsibility |
|-----------------|----------------|
| `main.py`       | Menu loop and application entry point. Handles all user input/output and routes to submenus (Member Management, Equipment Management, Loan Management, Reports). |
| `models.py`     | Domain classes: `Member`, `Equipment`, `Loan`. Each class holds its own data and behaviour, e.g. `Loan.is_overdue()` and `Loan.is_returned()`. |
| `database.py`   | All SQLite access lives here: connection setup, table creation, and every CRUD/report SQL function. No other file talks to SQLite directly. |
| `services.py`   | Business rules for checkout and return - decides whether an action is allowed (member exists? equipment available?) before touching the database. |
| `validation.py` | Input validation helpers for names, emails, IDs, and general text, each with a loop that keeps asking until valid input is given. |
| `makerspace.db` | The SQLite database file. Created automatically the first time the app runs - not something you need to set up manually. |

This is a layered structure: `main.py` only handles the menu and
user interaction, `services.py` holds the rules, `database.py` holds
the SQL, `validation.py` guards the input, and `models.py` provides
the OOP objects that tie it together.

## How to Run

1. Open a terminal in the project folder.
2. Run:
```bash
   python3 main.py
```
3. On first run, `makerspace.db` is created automatically with empty
   tables - no manual setup step is required.
4. Use the on-screen menu to navigate: choose a number for Member
   Management, Equipment Management, Loan Management, or Reports,
   then pick an option inside that submenu. Enter `0` at any submenu
   to return to the main menu, and `0` at the main menu to exit.

## Database Design

Three tables, linked by foreign keys:

- **members** - `id`, `name`, `email`
- **equipment** - `id`, `name`, `category`, `is_available`
- **loans** - `id`, `member_id`, `equipment_id`, `checkout_date`,
  `due_date`, `return_date`; `member_id` and `equipment_id` are
  foreign keys referencing `members(id)` and `equipment(id)`, with
  `ON DELETE CASCADE` so that if a member or equipment record is
  deleted, their related loan records are cleaned up automatically
  rather than left dangling. A database trigger also marks equipment
  as available again automatically if its loan record is deleted.

## Object-Oriented Design

- **`Member`** - stores `id`, `name`, `email`, and formats itself for
  display.
- **`Equipment`** - stores `id`, `name`, `category`, and
  `is_available` (converted from SQLite's 1/0 into a proper Python
  boolean); formats itself for display with an "Available" / "On
  Loan" status.
- **`Loan`** - stores loan details and provides behaviour methods:
  `is_returned()` checks whether the loan has a return date, and
  `is_overdue()` checks whether an unreturned loan's due date has
  passed. These objects are built from database rows and used
  throughout `main.py` and `services.py` rather than working with raw
  tuples everywhere.

## Input Validation

Every user input is validated before use, and the user is
re-prompted with a clear message until valid input is given, rather
than the program crashing on bad input:

- **Names** - must contain letters, cannot be purely numeric, cannot
  be empty
- **Emails** - must contain exactly one `@` with non-empty text on
  both sides, and a `.` in the domain part
- **IDs** - must be a positive whole number
- **General text** (equipment names, categories, search keywords) -
  same letter/non-empty rules as names

## Reports

Two SQL-driven reports are available from the Reports menu:

1. **Currently borrowed items** - every loan where `return_date` is
   still `NULL`, joined against `members` and `equipment` to show who
   has what and when it's due.
2. **Overdue loans** - the same active-loan query, filtered further
   to loans whose `due_date` has already passed.

## Example Workflow

1. Register a member.
2. Register a piece of equipment.
3. Check out that equipment to the member (Loan Management).
4. View it under "Currently borrowed items" (Reports).
5. Return the equipment - its status flips back to "Available".
6. Search or update records as needed.

## Data Persistence

`makerspace.db` lives in the project folder and is not reset between
runs - anything registered or checked out is still there the next
time you launch `python3 main.py`.

## AI Usage Disclosure

AI tools (ChatGPT and Claude) were used during development as
learning and debugging aids, specifically to:
- Explain coding errors and help debug issues
- Discuss design options for the database schema and class structure
- Improve the clarity of documentation and project organisation

All code was written and is understood by me, and I am able to
explain any part of it during the live demonstration.
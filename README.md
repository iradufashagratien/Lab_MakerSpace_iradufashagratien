# Campus MakerSpace Checkout System

This project is a Python command-line application for managing a campus makerspace checkout system. It allows staff/operators to manage members, equipment inventory, loans, validation, and reports using SQLite as the database backend.

## Project Overview

The system supports:
- registering members
- listing and searching members
- updating and deleting members
- registering equipment
- listing and searching equipment
- updating and deleting equipment
- checking out equipment to members
- returning equipment
- preventing invalid actions
- generating reports for active and overdue loans

## Project Structure

- `main.py` – menu-driven application entry point
- `models.py` – domain classes such as `Member`, `Equipment`, and `Loan`
- `database.py` – SQLite connection, schema creation, CRUD functions, and reports
- `services.py` – business logic for checkout and return rules
- `validation.py` – input validation for names, IDs, emails, and text fields
- `makerspace.db` – SQLite database file created automatically on first run

## Features

### Object-Oriented Design
The project uses classes with attributes and methods to model real-world objects:
- `Member` stores member information
- `Equipment` stores item information and availability status
- `Loan` stores loan information and checks whether an item is returned or overdue

### SQLite Database
The application uses SQLite to persist data between runs. The database contains tables for:
- `members`
- `equipment`
- `loans`

The `loans` table is linked to `members` and `equipment` using foreign keys, and deletes are managed safely so data remains consistent.

### Validation
The system checks user input before performing actions, including:
- names cannot contain numbers
- IDs must be positive integers
- emails must be valid
- equipment names and categories cannot be empty or numeric-only

### Reports
The application includes reports for:
- currently borrowed items
- overdue loans

## How to Run

1. Open a terminal in the project folder.
2. Run:

```bash
python3 main.py
```

3. Use the menu to manage members, equipment, loans, and reports.

## Example Workflow

1. Register a member.
2. Register equipment.
3. Checkout equipment to a member.
4. View active loans.
5. Return the equipment.
6. Search or update records as needed.

## Data Persistence

The SQLite database file is stored as `makerspace.db` in the project directory. It is created automatically when the app starts if it does not already exist.

## AI Usage

AI tools were used to help with this project in the following ways:
- explaining coding errors and debugging issues
- discussing design options for the database and class structure
- improving clarity of documentation and project organisation

This support helped improve the quality of the implementation and made the project easier to understand and maintain.

## Notes

This project is designed as a beginner-friendly CLI application and follows a simple layered structure:
- menu and user interaction in `main.py`
- object models in `models.py`
- data access in `database.py`
- business logic in `services.py`
- input validation in `validation.py`

This keeps the code organised and easier to explain during live demonstration.

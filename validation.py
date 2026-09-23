def is_valid_name(value):
    if value is None:
        return False

    value = value.strip()
    if value == "":
        return False

    try:
        int(value)
        return False
    except ValueError:
        pass

    if any(ch.isdigit() for ch in value):
        return False

    if not any(ch.isalpha() for ch in value):
        return False

    return True


def is_valid_text(value):
    if value is None:
        return False

    value = value.strip()
    if value == "":
        return False

    try:
        int(value)
        return False
    except ValueError:
        pass

    if any(ch.isdigit() for ch in value):
        return False

    if not any(ch.isalpha() for ch in value):
        return False

    return True


def is_valid_email(value):
    if value is None:
        return False

    value = value.strip()
    if value == "":
        return False

    if "@" not in value:
        return False

    parts = value.split("@")
    if len(parts) != 2:
        return False

    local_part, domain = parts
    if local_part == "" or domain == "":
        return False

    if "." not in domain:
        return False

    return True


def is_valid_id(value):
    if value is None:
        return False

    value = value.strip()
    if value == "":
        return False

    try:
        number = int(value)
    except ValueError:
        return False

    return number > 0


def get_valid_name(prompt):
    while True:
        try:
            value = input(prompt).strip()
            if is_valid_name(value):
                return value
            print("Invalid name. Please enter letters only, without numbers.")
        except EOFError:
            print("Invalid input.")
            return ""


def get_valid_email(prompt):
    while True:
        try:
            value = input(prompt).strip()
            if is_valid_email(value):
                return value
            print("Invalid email. Please enter a valid email address.")
        except EOFError:
            print("Invalid input.")
            return ""


def get_valid_id(prompt):
    while True:
        try:
            value = input(prompt).strip()
            if is_valid_id(value):
                return int(value)
            print("Invalid ID. Please enter a positive whole number.")
        except EOFError:
            print("Invalid input.")
            return 0


def get_valid_text(prompt, error_message):
    while True:
        try:
            value = input(prompt).strip()
            if is_valid_text(value):
                return value
            print(error_message)
        except EOFError:
            print("Invalid input.")
            return ""

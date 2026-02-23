import re


def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_name(name: str) -> bool:
    return len(name.strip()) >= 2


def validate_user_input(text: str, max_length: int = 3000) -> str:
    cleaned = text.strip()

    if len(cleaned) == 0:
        raise ValueError("Input cannot be empty.")

    if len(cleaned) > max_length:
        raise ValueError("Input too long.")

    return cleaned
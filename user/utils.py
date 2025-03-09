import re


def is_valid_email(email: str) -> bool:
    # Regular expression for validating email format
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Match the email against the regex
    if re.match(email_regex, email):
        return True
    return False
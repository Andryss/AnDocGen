from storage import normalize_email


def create_user(email: str) -> str:
    return normalize_email(email)

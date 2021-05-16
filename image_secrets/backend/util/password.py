"""Password hashing and other functions connected to passwords."""

import bcrypt


def hash_(plain: str) -> bytes:
    """Return password hashed with bcrypt.

    :param str plain: Password in plain text

    """
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())


def auth(plain: str, hashed: str) -> bool:
    """Authenticate a password hash with a plain text password.

    :param plain: New plain text password to authenticate
    :param hashed: Original password hash

    """
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False

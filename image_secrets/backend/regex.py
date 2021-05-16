"""Module with regular expressions."""
import re

INTEGRITY_FIELD = re.compile(r'"ix_users_(\w+)"')

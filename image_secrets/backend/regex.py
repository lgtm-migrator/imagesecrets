"""Module with regular expressions."""
import re

INTEGRITY_FIELD = re.compile(r"(?P<field>username|email)\)=\((?P<detail>[^)]+?)")

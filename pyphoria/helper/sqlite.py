""""Interface!!!!!! to sqlite."""

SQLITE_DB = 'data.db'

import sqlite3

from models import Character, Item, Monster
from sqlalchemy import create_engine

engine = create_engine("sqlite://sqlite.sqlite", echo=True)


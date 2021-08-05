import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(os.environ['DATABASE_URL'])


def create_table():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS entries (content TEXT, date TEXT);")


def add_entry(entry_content, entry_date):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO entries VALUES (%s, %s);", (entry_content, entry_date))


def get_entries():
    return entries

import os
import datetime
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    release_timestamp REAL NOT NULL
    );"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    id SERIAL NOT NULL PRIMARY KEY,
    watcher_name TEXT NOT NULL,
    title TEXT NOT NULL);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"

DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"

SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = %s;"

INSERT_WATCHED_MOVIE = "INSERT INTO watched (watcher_name, title) VALUES (%s, %s);"

SET_MOVIE_WATCHED = "UPDATE movies SET watched = TRUE WHERE title = %s;"

connection = psycopg2.connect(os.environ['DATABASE_URL'])


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_WATCHLIST_TABLE)


def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def watch_movie(watcher_name, title):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_MOVIE, (title,))
            cursor.execute(INSERT_WATCHED_MOVIE, (watcher_name,title))


def get_watched_movies(watcher_name):
    with connection:
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (watcher_name,))
            return cursor.fetchall()


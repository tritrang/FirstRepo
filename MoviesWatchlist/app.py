import datetime
import database

menu = """Please select one of the following options:
1. Add new movie.
2. View upcoming movies.
3. View all movies.
4. Watch a movie.
5. View watched movies.
6. Exit

Your selection: """
welcome = "Welcome to the watchlist app!"


# App starts here
print(welcome)
database.create_tables()


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(heading, movies):
    print(f"--{heading} movies--")
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie['release_timestamp'])
        human_date = movie_date.strftime("%b %d %Y")
        print(f"{movie['title']} released on {human_date}")
    print("---- \n")


def print_watched_movie_list(username, movies):
    print(f"--{username}'s watched movies--")
    for movie in movies:
        print(f"{movie['title']}")
    print("---- \n")


def prompt_watch_movie():
    movie = input("Enter title of the movie watched: ")
    watcher_name = input("Who watched the movie: ")
    database.watch_movie(watcher_name, movie)


while (user_input := int(input(menu))) != 6:
    if user_input == 1:
        prompt_add_movie()
    elif user_input == 2:
        movie_list = database.get_movies(upcoming=True)
        print_movie_list("Upcoming", movie_list)
    elif user_input == 3:
        movie_list = database.get_movies()
        print_movie_list("All", movie_list)
    elif user_input == 4:
        prompt_watch_movie()
    elif user_input == 5:
        watcher_name = input("What is the watcher's name? ")
        movie_list = database.get_watched_movies(watcher_name)
        print_watched_movie_list(watcher_name, movie_list)
    else:
        print("Invalid input. Please choose a valid option!")

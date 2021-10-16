"""
Project 1: Book Recommendations
Student: Tri Trang
I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""
from typing import List, AnyStr, Tuple, Dict
from operator import itemgetter
from pathlib import Path

"""Set up file paths for BookList.csv and Ratings.csv.
Please change the paths to the right directory(s) where you store the files before running this program."""

data_folder = Path().cwd()
BookList_path = data_folder / "BookList.txt"
Ratings_path = data_folder / "Ratings.txt"


"""Read booklist.txt into a list of (author,title) tuples.
Output: [(Douglas Adams,The Hitchhiker's Guide To The Galaxy), ...]"""
with open(BookList_path, 'r') as f1:
    book_list = f1.read().splitlines()
    author_book_list = [tuple(author_book.split(',')) for author_book in book_list]
# For testing purposes, please uncomment the print() function below.
# print(author_book_list)


"""Read ratings.txt into a dictionary keyed by reader name (converted to lower case). 
The value for each key is a list of the ratings for that reader, preserving the original order. 
Output: {name: [0,1,3,...], ...}"""
with open(Ratings_path, 'r') as f2:
    ratings = f2.read().splitlines()
    readers = []
    reader_ratings = {}
    for idx, line in enumerate(ratings):
        if idx % 2 == 0:
            readers.append(line.lower()) if line.lower() not in readers else None  # To get a list of unique readers
            reader_ratings[line.lower()] = ratings[idx + 1].strip().split(" ")
# For testing purposes, please uncomment the print() function below.
# print(readers)


def dot_prod(person: AnyStr, other_reader: AnyStr, rating_list: Dict) -> Tuple:
    """This function will calculate affinity scores between two friends.
    Returns a tuple of other_reader and associated affinity score (integer type)"""
    affinity_score = 0
    person_ratings = itemgetter(person)(rating_list)
    other_reader_ratings = itemgetter(other_reader)(rating_list)
    for person_rating, friend_rating in zip(person_ratings, other_reader_ratings):
        affinity_score += int(person_rating) * int(friend_rating)
    return other_reader, affinity_score
# For testing purposes, please uncomment the print() function below.
# print(dot_prod('reuven', 'ben', reader_ratings))


def get_two_friends(person: AnyStr) -> List:
    """Call dot_prod on all other readers to calculate affinity scores between the reader in question and them.
    Returns a sorted LIST of the names of the 2 readers with the highest affinity scores
    compared to the reader in question. Use the SORTED function to sort those names before returning."""
    other_readers_list = [reader for reader in readers if reader != person]
    other_reader_rating_list = []
    for other_reader in other_readers_list:
        other_reader_rating_list.append(dot_prod(person, other_reader, reader_ratings))
    two_friends = sorted(other_reader_rating_list, key=itemgetter(1), reverse=True)[:2]
    two_friend_names = [(friend[0], friend[1]) for friend in two_friends]
    return two_friend_names
# For testing purposes, please uncomment the print() function below.
# print(get_two_friends('francois'))


def sort_book(author_book) -> Tuple:
    """This function serves as the key in the SORT method used below."""
    author = author_book[0].split(" ")
    book = author_book[1]
    author_first_name = author[0]
    author_last_name = author[-1]
    return author_last_name, author_first_name, book


def recommend(person, rating_list: Dict) -> List:
    """Call get_two_friends and then get the recommended books from the 2 friends obtained.
    Book requirements:
        - The reader in question hasn't yet read
        - The 2 friends have rated 3 or 5
    Returns a LIST of pairs/tuples containing the (author, title) of all the recommended books.
    This list is sorted first by author last name, then author first name, and then by title.
    """

    two_friend_names = [friend[0] for friend in get_two_friends(person)]

    person_ratings = itemgetter(person)(rating_list)

    friends_one_ratings = itemgetter(two_friend_names[0])(rating_list)

    friends_two_ratings = itemgetter(two_friend_names[1])(rating_list)

    friend_one_books_rated_high_idx = [int(index) for index, rating in enumerate(friends_one_ratings) if int(rating) >= 3]

    friend_two_books_rated_high_idx = [int(index) for index, rating in enumerate(friends_two_ratings) if int(rating) >= 3]

    books_rated_high_by_friends_idx = [index for index in friend_one_books_rated_high_idx]

    for book_idx in friend_two_books_rated_high_idx:
        if book_idx not in friend_one_books_rated_high_idx:
            books_rated_high_by_friends_idx.append(book_idx)

    person_books_not_read_idx = [int(index) for index, rating in enumerate(person_ratings) if int(rating) == 0]

    books_rated_high_by_friends_idx = sorted(books_rated_high_by_friends_idx)

    recommended_books_idx = [index for index in person_books_not_read_idx if index in books_rated_high_by_friends_idx]

    recommended_books = [book for index, book in enumerate(author_book_list) if index in recommended_books_idx]

    recommended_books.sort(key=sort_book)

    return recommended_books
# For testing purposes, please uncomment the print() function below.
# print(recommend('ben', reader_ratings))


def main():
    person = str(input("Who are you recommending books to? ").lower())

    if person in readers:
        print("----------------------------------------")
        print("Two friends with highest affinity scores are: ")
        for friend, score in get_two_friends(person):
            print(f"- {friend.title()} who has {score} affinity score compared to {person.title()}")
        print("----------------------------------------")
        print("Recommended books are: ")
        for author, book in recommend(person, reader_ratings):
            print(f"- {book} by {author}")
    else:
        print("----------------------------------------")
        print(f"{person.title()} doesn't exist in ratings.txt")
        print("----------------------------------------")
        print("Here is a list of names that currently exist in ratings.txt")
        count = 0
        for name in readers:
            count += 1
            print(f"{count}. {name.title()}")


if __name__ == "__main__":
    main()

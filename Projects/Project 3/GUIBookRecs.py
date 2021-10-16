"""
Project 3: Book Recommendations GUI
Student: Tri Trang
I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""
from breezypythongui import EasyFrame
from bookrecs import *


class BookRecs(EasyFrame):
    def __init__(self):
        super().__init__(title="Book Recommendation", width=300, height=100, background="#B0E0E6", resizable=True)
        self.name = ""
        self.report = ""
        self.btn_find_friend = self.addButton(text="Friend", row=0, column=0, command=self.get_person)
        self.btn_recommend = self.addButton(text="Recommend", row=0, column=1, command=self.get_recommendation)
        self.btn_get_report = self.addButton(text="Report", row=0, column=2, command=self.get_all_recommendations)

    def get_person(self):
        self.name = self.prompterBox(title="Friend", promptString="Enter Reader Name: ").lower()
        if self.name in readers:
            friends = get_two_friends(self.name)
            name_friends = "\n".join([friend[0].title() for friend in friends])

            self.messageBox(title=f"Friends of {self.name.title()}", message=f"{name_friends}", width=50, height=10)
        else:
            self.messageBox(title="Error", message="No such reader.")

    def get_recommendation(self):
        self.name = self.prompterBox(title="Friend", promptString="Enter Reader Name: ").lower()
        if self.name in readers:
            recommended_books = recommend(self.name, reader_ratings)
            books = "\n".join([book[0] + ", " + book[1] for book in recommended_books])
            self.messageBox(title=f"Recommendations for {self.name.title()}", message=f"{books}", width=50, height=10)
        else:
            self.messageBox(title="Error", message="No such reader.")

    def get_all_recommendations(self):
        for person in readers:
            friends = get_two_friends(person)
            recommended_books = recommend(person, reader_ratings)
            books = "\n        ".join([book[0] + ", " + book[1] for book in recommended_books])
            self.report += f"""Recommendations for {person.title()} from {friends[0][0].title()} and {friends[1][0].title()}:
        {books}
            
"""
        self.messageBox(title="Report", message=f"{self.report}", width=100, height=70)


def main():
    BookRecs().mainloop()


if __name__ == '__main__':
    main()


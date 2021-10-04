"""
Project 3: Coffee Machine
Student: Tri Trang
I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""


class Product:
    def __init__(self, name, price, recipe):
        self.name = name
        self.price = price
        self.recipe = recipe

    def __str__(self):
        return f"{self.name}, ${self.price} cents, {self.recipe}"

    def get_price(self):
        return self.price

    def make(self):
        print(f"Making {self.name}")
        for ingredient in self.recipe:
            print(f"Dispensing {ingredient}")


class CashBox:
    def __init__(self):
        self.total_received = 0
        self.credit = 0

    def deposit(self, amount):
        if amount in (50, 25, 10, 5):
            self.credit += amount
            return f"Depositing {amount}. You have {self.credit} cents credit"
        else:
            return "We only take half_dollars, quarters, dimes, and nickles."

    def return_coins(self):
        return_amount = self.credit
        self.credit -= self.credit
        return f"Returning ${return_amount} cents"

    def have_you(self, product_price):
        if self.credit > product_price:
            return True
        else:
            return False

    def deduct(self, product_price):
        self.total_received += product_price
        change = self.credit - product_price
        self.credit -= (change + product_price)
        return f"Returning {change} cents."

    def total(self):
        return self.total_received


class Selector:
    def __init__(self):
        black = Product("Black", 35, ["cup", "coffee", "water"])
        white = Product("White", 35, ["cup", "coffee", "creamer", "water"])
        sweet = Product("Sweet", 35, ["cup", "coffee", "sugar", "water"])
        white_and_sweet = Product("White & Sweet", 35, ["cup", "coffee", "sugar", "creamer", "water"])
        bouillon = Product("Bouillon", 25, ["cup", "bouillon powder", "water"])
        self.products = [black, white, sweet, white_and_sweet, bouillon]
        self.cash_box = CashBox()

    def select(self, choice_index):
        product_price = self.products[choice_index - 1].get_price()
        if self.cash_box.have_you(product_price):
            self.products[choice_index - 1].make()
            return self.cash_box.deduct(product_price)
        else:
            return "Sorry. Not enough money deposited."


class CoffeeMachine:
    def __init__(self):
        print("PRODUCT LIST: all 35 cents, except bouillon (25 cents)")
        print("1=black, 2=white, 3=sweet, 4=white & sweet, 5=bouillon")
        print("Sample commands: insert 25, select 1.")
        self.command = ""
        self.action_choice = []
        self.action = ""
        self.choice = 0
        self.selector = Selector()

    def one_action(self):
        self.command = input("Your command: ").lower()
        self.action_choice = self.command.split()
        self.action = self.action_choice[0]
        self.choice = int(self.action_choice[1]) if len(self.action_choice) > 1 else None
        return True

    def total_cash(self):
        return self.selector.cash_box.total_received


if __name__ == '__main__':

    m = CoffeeMachine()
    while m.one_action():
        if m.action == "quit":
            break
        elif m.action == "insert":
            print(m.selector.cash_box.deposit(m.choice))
        elif m.action == "select" and 1 <= m.choice <= 5:
            print(m.selector.select(m.choice))
        elif m.action == "cancel":
            print(m.selector.cash_box.return_coins())
        else:
            print("Invalid command.")
    total = m.total_cash()
    print(f"Total cash: ${total/100:.2f}")



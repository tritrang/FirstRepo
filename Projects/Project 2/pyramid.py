"""
Project 1: Human Pyramids
Student: Tri Trang
I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""
import sys
from time import perf_counter
func_count = 0
cache = {}
cache_hit = 0


def weight_on(row, column):
    """
    Reference Demonstration:
                     A
                    / \
                   B   C
                  / \ / \
                 D   E   F
                / \ / \ / \
               G   H   I   J

    For this assignment, I have noticed that we can use 1 base case and 3 different recursive cases to solve the problem

    Base Case: WHEN row == 0 (column is also automatically 0) THEN weight_on = 0.00

    First Recursive Case: WHEN column = 0 THEN weight_on(row, column) = (200 + weight_on(row - 1, column)) / 2
        For example, Person D carries half of Person B's body weight plus half of the weight Person B is holding up
        => Weight_on_D = 200/2 + Weight_on_B/2
                       = 100 + Weight_on_B/2

    Second Recursive Case: WHEN column = row THEN weight_on(row, column) = (200 + weight_on(row - 1, column - 1)) / 2
        Similar to First Recursive Case, Person F carries half of Person C's body weight plus half of the weight Person
        C is holding up
        => Weight_on_F = 200/2 + Weight_on_C/2
                       = 100 + Weight_on_C/2

    Third Recursive Case: WHEN 0 < column < row. This is a little bit more complex.
        For this case, we are looking at Person H and Person I.
        Person H carries half of Person D's body weight plus half of the weight Person B is holding up. On top of that,
        Person H also carries half of Person E's body weight plus half of the weight Person E is holding up.
        Weight_on_H = (200 + Weight_on_D)/2 + (200 + Weight_on_E)/2
                    = 200 + (Weight_on_D + Weight_on_E)/2
        Same thing for Person I, Person I carries half of Person E's body weight plus half of the weight Person E is
        holding up. Additionally, Person I also carries half of Person F's body weight plus half of the weight Person F
        is holding up.
        Weight_on_I = (200 + Weight_on_E)/2 + (200 + Weight_on_F)/2
                    = 200 + (Weight_on_E + Weight_on_F)/2
        We can see the pattern here:
         weight_on(row, column) = 200 + (weight_on(row - 1, column - 1) + weight_on(row - 1, column)) / 2
    """
    global func_count, cache, cache_hit
    func_count += 1
    if (row, column) in cache:
        cache_hit += 1
        return cache[(row, column)]
    else:
        if column > row or column < 0 or row < 0:
            print("No such person in given coordinate exists")
        else:
            a = 0
            # Base Case
            if column == 0 and row == 0:
                None

            # First Recursive Case
            elif column == 0 and row:
                a = 100 + weight_on(row - 1, column)/2

            # Second Recursive Case
            elif column == row and row:
                a = 100 + weight_on(row - 1, column - 1)/2

            # Third Recursive Case
            else:
                a = 200 + (weight_on(row - 1, column - 1) + weight_on(row - 1, column)) / 2
            cache[(row, column)] = a
            return a


def human_pyramid(rows):
    """This function returns a list of lists"""
    new_rows = []
    for row in range(rows):
        row_element = []
        for column in range(row + 1):
            row_element.append(weight_on(row, column))
        new_rows.append(row_element)
    return new_rows


def main(num_row):
    global func_count, cache, cache_hit
    time_start = perf_counter()
    for row in human_pyramid(num_row):
        for weight in row:
            print(f"{weight:.2f}", end=' ')
        print('\r')
    time_end = perf_counter()
    print(f"Elapsed time: {time_end - time_start} seconds")
    print(f"Number of function calls: {func_count}")
    print(f"Number of cache hits: {cache_hit}")


if __name__ == '__main__':
    main(int(sys.argv[1]))

"""
Project 5: Payroll
Student: Tri Trang
I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""
import abc
import os
from pathlib import Path

PAY_LOGFILE = "paylog.txt"
data_folder = Path().cwd()
employees_path = data_folder / "employees.csv"
timecards_path = data_folder / "timecards.csv"
receipts_path = data_folder / "receipts.csv"


class Employee:
    def __init__(self, emp_id, first_name, last_name, address, city, state, zipcode):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.classification = None

    def __repr__(self):
        return f"({self.emp_id}, {self.first_name}, {self.last_name}, {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.classification})"

    def make_hourly(self, hourly_rate):
        self.classification = Hourly(hourly_rate)

    def make_salaried(self, salary):
        self.classification = Salaried(salary)

    def make_commissioned(self, salary, commission_rate):
        self.classification = Commissioned(salary, commission_rate)

    def issue_payment(self):
        amount = self.classification.compute_pay()
        if amount > 0:
            with open(PAY_LOGFILE, 'a') as file:
                file.write(f"Mailing {amount} to {self.first_name} {self.last_name} at {self.address} {self.city} {self.state} {self.zipcode}\n")

            """Clear employees' respective timecards and receipts list afterward, so these entries won't be used 
            again for the next pay period """

            with open(timecards_path, 'w') as file:
                file.truncate()
            with open(receipts_path, 'w') as file:
                file.truncate()
        else:
            pass


class Classification(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def compute_pay(self):
        pass


class Hourly(Classification):
    def __init__(self, hourly_rate):
        self.hourly_rate = hourly_rate
        self.hours_worked = []

    def __repr__(self):
        return f"Hourly, {self.hourly_rate}"

    def compute_pay(self):
        return round(float(self.hourly_rate) * sum([float(hour) for hour in self.hours_worked]), 2)

    def add_timecard(self, hours):
        self.hours_worked.append(hours)


class Salaried(Classification):
    def __init__(self, salary):
        self.salary = salary

    def __repr__(self):
        return f"Salaried, {self.salary}"

    def compute_pay(self):
        return round(float(self.salary)/24, 2)


class Commissioned(Salaried):
    def __init__(self, salary, commission_rate):
        super().__init__(salary)
        self.commission_rate = commission_rate
        self.receipts = []

    def __repr__(self):
        return f"Commissioned, {self.salary}, {self.commission_rate}"

    def compute_pay(self):
        return round(float(self.salary)/24 + sum([float(receipt) for receipt in self.receipts])*int(self.commission_rate)/100.0, 2)

    def add_receipt(self, receipt):
        return self.receipts.append(receipt)


def load_employees():
    emp_list = []
    final_emp_list = []
    with open(employees_path, 'r') as f:
        f = f.read().splitlines()
    for emp in f:
        emp_list.append(tuple(emp.split(",")))

    emp_list = emp_list[1:]

    for emp_info in emp_list:
        temp_emp_holder = Employee(emp_info[0], emp_info[1], emp_info[2], emp_info[3], emp_info[4], emp_info[5], emp_info[6])
        if emp_info[7] == '1':
            temp_emp_holder.make_salaried(emp_info[8])
        elif emp_info[7] == '2':
            temp_emp_holder.make_commissioned(emp_info[8], emp_info[9])
        else:
            temp_emp_holder.make_hourly(emp_info[10])
        final_emp_list.append(temp_emp_holder)

    return final_emp_list


# print(load_employees())


def find_employee_by_id(emp_id):
    found_employee = None
    for employee in employees:
        if employee.emp_id == emp_id:
            found_employee = employee
        else:
            pass
    return found_employee


def process_timecards():
    emp_hours_list = []
    with open(timecards_path, 'r') as f1:
        f1 = f1.read().splitlines()
    for record in f1:
        emp_hours_list.append(tuple(record.split(",")))

    for employee in employees:
        for record in emp_hours_list:
            if isinstance(employee.classification, Hourly) and employee.emp_id == record[0]:
                employee.classification.hours_worked.extend(record[1:])
            else:
                pass


def process_receipts():
    emp_receipts_list = []
    with open(receipts_path, 'r') as f2:
        f2 = f2.read().splitlines()
    for record in f2:
        emp_receipts_list.append(tuple(record.split(",")))

    for employee in employees:
        for record in emp_receipts_list:
            if isinstance(employee.classification, Commissioned) and employee.emp_id == record[0]:
                employee.classification.receipts.extend(record[1:])
            else:
                pass


def run_payroll():
    if os.path.exists(PAY_LOGFILE):
        os.remove(PAY_LOGFILE)
    for emp in employees:
        emp.issue_payment()


employees = load_employees()




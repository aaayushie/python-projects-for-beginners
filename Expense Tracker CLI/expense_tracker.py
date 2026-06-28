import json
from typing import List
from expense import Expense

import calendar
import datetime

def main():
    print("Expense Tracker")
    expense_file_path = "expenses.json"
    budget = 3000


    while True:
        print("\nChoose an option:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses")
        print("4. View Summary")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            expense = get_user_expense()
            print(expense)
            save_expense_to_json(expense, expense_file_path)

        elif choice == "2":
            view_expenses(expense_file_path)

        elif choice == "3":
            filter_expenses(expense_file_path)

        elif choice == "4":
            summarize_expenses(expense_file_path, budget)

        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice! Please try again.")


def get_user_expense():
    print(f"Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))                       
    
    expense_category = ["Food", "Home", "Work", "Fun", "Miscellaneous"]
    
    while True:
        print("Slect a category: ")
        for i, category_name in enumerate(expense_category):
            print(f"  {i + 1}. {category_name}")
        
        value_range = f"[1 - {len(expense_category)}]"
        selected_index = int(input(f"Enter category number {value_range}: ")) - 1

        if selected_index in range(len(expense_category)):
            selected_category = expense_category[selected_index]
            new_expense = Expense(
                name = expense_name, category = selected_category, amount = expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")
        

def save_expense_to_json(expense: Expense, expense_file_path):
    print(f"Savinng User Expense: {expense}")

    try:
        with open(expense_file_path, "r") as f:
            expenses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    expenses.append({
        "name": expense.name,
        "category": expense.category,
        "amount": expense.amount
    })

    with open(expense_file_path, "w") as f:
        json.dump(expenses, f, indent=4)
    


def view_expenses(expense_file_path):
    print("\n===== All Expenses =====")

    try:
        with open(expense_file_path, "r") as f:
            expenses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No expenses found!")
        return

    for expense in expenses:
        print("----------------------------")
        print(f"Name     : {expense['name']}")
        print(f"Category : {expense['category']}")
        print(f"Amount   : ${expense['amount']:.2f}")
        print("----------------------------")


def filter_expenses(expense_file_path):
    print("\n=== Filter Expenses ===")

    user_category = input("Enter category: ")

    try:
        with open(expense_file_path, "r") as f:
            expenses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No expenses found!")
        return

    found = False

    for expense in expenses:
        if expense["category"].lower() == user_category.lower():
            print("----------------------------")
            print(f"Name     : {expense['name']}")
            print(f"Category : {expense['category']}")
            print(f"Amount   : ${expense['amount']:.2f}")
            print("----------------------------")
            found = True

    if not found:
        print("No matching expenses found.")



def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing User Expense")
    expenses: List[Expense] = []

    try:
        with open(expense_file_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No expenses found!")
        return

    for item in data:
        expenses.append(
            Expense(
                name=item["name"],
                category=item["category"],
                amount=float(item["amount"])
            )
        )
  
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("Expenses By Category:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")
   
    total_spent = sum([x.amount for x in expenses])
    print(f"Total spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent 
    print(f"Budget Remaining: ${remaining_budget:.2f}")


    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(f"Budget Per Day: ${daily_budget:.2f}")

if __name__ == "__main__":
    main()
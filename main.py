import json


def main():
    expenses = load_expenses()

    while True:
        try:
            print("=============================")
            print("  PERSONAL EXPENSE TRACKER  ")
            print("=============================\n")

            print("1. Add expense")
            print("2. View expenses")
            print("3. View total spending")
            print("4. View spending by category")
            print("5. Edit an existing expense")
            print("6. Delete an existing expense")
            print("7. Exit")

            selection = int(input("\nSelect an option: "))
            print()

            if selection == 1:
                add_expense(expenses)

            elif selection == 2:
                view_expenses(expenses)

            elif selection == 3:
                total = calculate_total(expenses)

                print("=============================")
                print("       TOTAL SPENDING        ")
                print("=============================")

                print(f"\nTotal expenses: ${total:.2f}\n")

            elif selection == 4:
                spending = calculate_category_spending(expenses)

                if spending:
                    for item in spending:
                        amount = spending[item]
                        print(f"{item}: ${amount:.2f}")
                    print()

                else:
                    print("No expenses listed yet.")

            elif selection == 5:
                edit_expense(expenses)

            elif selection == 6:
                delete_expense(expenses)

            elif selection == 7:
                print("Goodbye!")
                break

            else:
                print("Invalid input\n")

        except ValueError:
            print("\nInvalid input\n")


def add_expense(expenses):
    while True:
        try:
            stored_expense = {}
            amount = float(input("What is the amount? "))

            if amount <= 0:
                print("Amount must be greater than zero.")

            else:
                stored_expense["Amount"] = amount
                category = input("What's the category? ").strip().title()

                if len(category) == 0:
                    print("Please insert a category")

                else:
                    stored_expense["Category"] = category
                    description = input("What's the description? ").strip()

                    if len(description) == 0:
                        print("Please insert a description")

                    else:
                        print("\nExpense added successfully!\n")
                        stored_expense["Description"] = description
                        expenses.append(stored_expense)
                        save_expenses(expenses)
                        break

        except ValueError:
            print("Invalid input")


def view_expenses(expenses):
    if not expenses:
        print("\nThere are no expenses to display\n")
        return

    for index, expense in enumerate(expenses, start=1):
        print("Expense #", index, sep="")

        amount = expense["Amount"]
        print(f"Amount: ${amount:.2f}")
        print("Category:", expense["Category"])
        print("Description:", expense["Description"])
        print()


def calculate_total(expenses):
    total = 0

    for expense in expenses:
        total = total + expense["Amount"]

    return total


def calculate_category_spending(expenses):
    spending = {}

    for expense in expenses:
        category = expense["Category"]
        amount = expense["Amount"]

        if category in spending:
            spending[category] = spending[category] + amount

        else:
            spending[category] = amount

    return spending


def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


def edit_expense(expenses):
    if not expenses:
        print("There are no expenses to edit.")
        return

    view_expenses(expenses)
    print("Which expense would you like to edit?\n")

    while True:
        try:
            number = int(input("Enter expense number: "))

            if 0 < number <= len(expenses):
                selected_expense = expenses[number - 1]

                print("\nWhat would you like to edit?\n")
                print("1. Amount")
                print("2. Category")
                print("3. Description")
                print("4. Cancel\n")

                selection = int(input("Select: "))

                if selection == 1:
                    print("You selected Amount.")
                    print(f"Current value: ${selected_expense['Amount']}")

                    while True:
                        try:
                            new_amount = float(input("Enter new amount: $"))

                            if new_amount > 0:
                                selected_expense["Amount"] = new_amount
                                print("Expense amount updated successfully!\n")
                                save_expenses(expenses)
                                return

                            else:
                                print("Invalid amount. Please try again.")

                        except ValueError:
                            print("Invalid amount. Please try again.")

                elif selection == 2:
                    print("You selected Category.")
                    print(f"Current value: {selected_expense['Category']}")

                    while True:
                        new_category = input(
                            "Enter new category: "
                        ).strip().title()

                        if new_category != "":
                            selected_expense["Category"] = new_category
                            print("Expense category updated successfully!\n")
                            save_expenses(expenses)
                            return

                        else:
                            print("Invalid input. Please try again.")

                elif selection == 3:
                    print("You selected Description.")
                    print(f"Current value: {selected_expense['Description']}")

                    while True:
                        new_description = input("Enter new description: ").strip()

                        if new_description != "":
                            selected_expense["Description"] = new_description
                            print("Expense description updated successfully!\n")
                            save_expenses(expenses)
                            return

                        else:
                            print("Invalid input. Please try again.")

                elif selection == 4:
                    print("Editing cancelled.\n")
                    return

                else:
                    print("You have provided an invalid input.")

            else:
                print("Please provide a valid expense number.")

        except ValueError:
            print("Please provide a valid expense number.")


def delete_expense(expenses):
    if not expenses:
        print("There are no expenses to delete.")
        return

    view_expenses(expenses)
    print("Which expense would you like to delete?\n")

    while True:
        try:
            number = int(input("Enter expense number: "))

            if 1 <= number <= len(expenses):
                selection = input(f"Are you sure you want to delete expense #{number}? (y/n): ").strip().lower()
                number = number - 1

                if selection == 'y':
                    expenses.pop(number)
                    save_expenses(expenses)
                    print("Expense deleted successfully!\n")
                    return

                elif selection == 'n':
                    print("Deletion cancelled.")
                    return

                else:
                    print("Please select one of the options.")

            else:
                print("Please provide a valid expense number.")

        except ValueError:
            print("Please provide a valid expense number.")


if __name__ == "__main__":
    main()
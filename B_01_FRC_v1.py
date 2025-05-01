import pandas
from tabulate import tabulate
from datetime import date


# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""
    return f"{decoration * 3} {statement} {decoration * 3}"

def yes_no_check(question):
    """Checks that users enter yes / y or no / n to a question"""

    while True:
        response = input(question).lower()

        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes (y) or no (no).\n")


def instructions():
    make_statement("Discipline", "😊")

    print('''

For each ticket holder enter..)
- Their mame
- Their age
- The payment method (cash / credit)

The program will record the ticket sale and calculate the
ticket cost (and the profit)

Once you have either sold all of the tickets or entered the
exit code ('xxx'), the program will display the ticket
sales information and write the data to a text file

It will also choose one lucky ticket holder who wins the 
draw (their ticket is free).

    ''')


def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank.  Please try again. \n")


def num_check(question, num_type="float", exit_code=None):
    """Checks users enter ana integer / float that is more than
    zero (or the optional exit code)"""

    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:

        response = input(question)

        # check for exit code and return it if entered
        if response == exit_code:
            return response

        # check datatype is correct and that number
        # is more than zero
        try:

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


def get_expenses(exp_type, how_many=1):
    """Gets variables / fixed expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    # Expenses dictionary
    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$ / Item": all_dollar_per_item
    }

    # defaults for fixed expenses
    amount = how_many  # how_many defaults to 1
    how_much_question = "How_much? $"

    # loop to get expenses
    while True:

        # Get item name and check it's not blank
        item_name = not_blank("Item Name: ")

        # check users enter at least one variable expense
        if exp_type == "variable" and item_name == "xxx" and len(all_items) == 0:
            print("Oops - you have not entered anything. "
                  "You need at least one item. ")
            continue

        # end loop when users enter exit code
        elif item_name == "xxx":
            break

        # Get variable expenses item amount <enter> default to number of
        # product being made
        if exp_type == "variable":
            amount = num_check(f"How many <enter> for {how_many}>: ",
                               "integer", "")

        # Allow users to push <enter> to default to number of items being made
        if amount == "":
            amount = how_many

        how_much_question = "Price for one? $"

        # Get price for item (question customised depending on expense type)
        price_for_one = num_check(how_much_question, "float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(price_for_one)

    # make panda
    expense_frame = pandas.DataFrame(expenses_dict)

    # Calculate Cost Column
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    # Calculate subtotal
    subtotal = expense_frame['Cost'].sum()

    # Apply currency formatting to currency columns.
    add_dollars = ['Amount', '$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # make expense frame into s string with the desired column
    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return expense_string, subtotal


def currency(x):
    """Formats numbers as currency ($#.###)"""
    return "{:.2f}".format(x)


# Main routine goes here

# initialise variables...

# assume we have no fixed expenses for now
fixed_subtotal = 0
fixed_panda_string = ""

print(make_statement("Fund Raising Calculator", "👌"))

print()
want_instruction = yes_no_check("Do you wat to see the instructions")
print()

if want_instruction == "yes":
    instructions()

print()

# Get product details...
product_name = not_blank("Product Name: ")
quantity_made = num_check("Quantity being made: ", "integer")

# Get variable expense...
print("Let's get the variable expense...")
variable_expenses = get_expenses("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

# ask users if they have fixed expenses and retrieve them
print()
has_fixed = yes_no_check("Do you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expenses("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    # if the users has not entered any fix expenses,
    # # set empty panda to "" so that it does not display!
    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"

# Get profit Goal here.

# string / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("xd")
month = today.strftime("Xm")
year = today.strftime("XY")

# Headings / strings...
main_heading_string = make_statement(f"Fund Raising Calculator "
                                     f"({product_name}, {day}/{month}/{year})", "=")
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement("Variable Expense", "=")
variable_subtotal_string = f"Variable Expense Subtotal: ${variable_subtotal:.2f}"

# set up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement("Fixed Expense", "-")
    fixed_subtotal_string = f"Fixed Expense Subtotal: {fixed_subtotal:.2f}"

# set fixed cost strings to blank if we don't have fixed costs
else:
    fixed_heading_string = make_statement("You have no fixed Expenses", "-")
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"

# List of strings to be outputted / written to file
to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, total_expenses_string]

# Print area
print()
for item in to_write:
    print(item)

# create file to hold data (add .txt extension)
file_mame = f"{product_name}_{year}_{month}_{day}"
write_to = f"{file_mame}.txt"

text_file = open(write_to, "w+")

# write the item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")

import sqlite3
import hashlib
from datetime import datetime


# Function to create the SQLite database and table
def create_database():
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (username text, hashed_password text, pizza_ordered text, quantity integer, time text, cost real)''')
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''SELECT hashed_password FROM orders WHERE username = ?''', (username,))
    result = c.fetchone()

    if result:
        hashed_password = result[0]
        input_password_hash = hashlib.sha256(password.encode()).hexdigest()

        if hashed_password == input_password_hash:
            print("User login successful!")
        else:
            print("Incorrect password. Please try again.")
    else:
        print("User not found. Please register first.")

    conn.close()

# Function to add a pizza order to the SQLite database
def add_order_to_database(username, hashed_password, pizza_ordered, quantity, time):
    cost = calculate_cost(pizza_ordered, quantity)

    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)''',
              (username, hashed_password, pizza_ordered, quantity, str(time), cost))
    conn.commit()
    conn.close()
    print("Order added to the database successfully!")


def get_order_history(username):
    conn = sqlite3.connect('pizza_orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE username = ?", (username,))
    orders = cursor.fetchall()

    if len(orders) == 0:
        print("No orders found for this user.")
    else:
        for order in orders:
            print(f"Order ID: {order[0]}, Pizza: {order[2]}, Cost: {order[3]}, Amount: {order[4]}, Time: {order[5]}")

# Function to calculate the cost of the order
def calculate_cost(pizza_ordered, quantity):
    # Add your own logic here to calculate the cost based on pizza and quantity
    cost_per_pizza = 10  # Example cost per pizza
    return cost_per_pizza * quantity


# Main program loop

print("WELCOME TO FATTY MAN PIZZA ORDERING SYSTEM!")
print("1. Register")
print("2. Login")
print("Press 'h' for help")

while True:

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        create_database()  # Create the database if not already exist
        add_order_to_database(username, hashed_password, "-", 0, datetime.now())
        print("User registered successfully!")

    elif choice == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        verify_user(username, password)
        print("(1) Order Pizza")
        print("(2) Get history")
        while True:
            A = input(": ")
            if A == '2':
                get_order_history(username)
            if A == '1':
                basket = ['', 'Pepperoni', 'Margarita','Love']
                print("(1) - Pepperoni")
                print("(2) - Margarita")
                print("(3) - Love")
                pizza_ordered = int(input(": "))
                pizza_ordered = basket[pizza_ordered]
                quantity = 1
                time = datetime.now()

                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                add_order_to_database(username, hashed_password, pizza_ordered, quantity, time)

        pass

    elif choice == 'h':
        print("yes, you need help with your godless pizza eating spree, don't kill yourself you lazy fatty")
        pass

    elif choice == '4':
        print("Thank you for using Pizza Ordering System. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
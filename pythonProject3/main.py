import sqlite3
import hashlib
from pizza_ordering import ordering
from registration import registration
import argparse
from datetime import datetime


def verify_user(username, password):
    try:
        conn = sqlite3.connect('pizza_orders.db')
        c = conn.cursor()
        c.execute('''SELECT hashed_password FROM users WHERE username = ?''', (username,))
        result = c.fetchone()

        if result:
            hashed_password = result[0]
            input_password_hash = hashlib.sha256(password.encode()).hexdigest()

            if hashed_password == input_password_hash:
                print('User login successful!')
            else:
                print('Incorrect password. Please try again.')
                conn.close()
                return False
        else:
            print('User not found. Please register first.')
            conn.close()
            return False
        conn.close()
        return True
    except Exception:
        print('User not found. Please register first.')
        return False


def get_order_history(username):
    try:
        conn = sqlite3.connect('pizza_orders.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE username = ?', (username,))
        orders = cursor.fetchall()

        if len(orders) == 0:
            print('No orders found for this user.')
        else:
            for order in orders:
                print(f'Order ID: {order[0]}, Pizza: {order[2]}, Quantity: {order[5]},'
                      f' Time: {order[6]}, Delivery time: {order[7]}, Cost: {order[8]}')
    except Exception:
        print('No orders found for this user.')


def get_order_status(username):
    try:
        conn = sqlite3.connect('pizza_orders.db')
        c = conn.cursor()
        c.execute('''SELECT delivery_time FROM orders WHERE username = ?''', (username,))
        result = c.fetchall()[-1][0]
        delivery_time = datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
        c.execute('''SELECT time FROM orders WHERE username = ?''', (username, ))
        result = c.fetchall()[-1][0]
        time = datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
        c.execute('''SELECT id FROM orders WHERE username = ?''', (username,))
        id = c.fetchall()[-1][0]
        current_time = datetime.now().replace(microsecond=0)
        if (current_time - time).total_seconds() / 60 > 20 and current_time < delivery_time:
            print(f"The order {id} is being delivered")
        elif current_time > delivery_time:
            print(f"The order {id} is delivered")
        elif (current_time - time).total_seconds() / 60 < 20:
            print(f"The order {id} is being cooked")
    except Exception:
        print('There are no orders')


def print_main_menu():
    print('1. Register\n2. Login\nPress "h" for help')


# Main program loop
def main():
    print('WELCOME TO FATTY MAN PIZZA ORDERING SYSTEM!')
    print_main_menu()
    while True:
        choice = input('Enter your choice: ')
        if choice == '1':
            registration()
        elif choice == '2':
            username = input('Enter username: ')
            password = input('Enter password: ')

            if not verify_user(username, password):
                continue
            select_option(username)
            pass

        elif choice == 'h':
            print('yes, you need help with your godless pizza eating spree, do not kill yourself you lazy fatty')
            pass

        elif choice == '4':
            print('Thank you for using Pizza Ordering System. Goodbye!')
            break

        else:
            print('Invalid choice. Please try again.')


def select_option(username):
    while True:
        print('(1) Order Pizza')
        print('(2) Get history')
        print('(3) Get the order status')
        print('(4) Log out')
        option = input(': ')
        if option == '1':
            ordering(username)
        elif option == '2':
            get_order_history(username)
        elif option == '3':
            get_order_status(username)
        elif option == '4':
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fatty Man Pizza Ordering System')
    parser.add_argument('--username', help='Username for login')
    parser.add_argument('--password', help='Password for login')

    args = parser.parse_args()

    if args.username and args.password:
        if not verify_user(args.username, args.password):
            print('Login failed. Please try again.')
            username = registration()
            select_option(username)
        else:
            username = args.username
            select_option(username)
    else:
          main()

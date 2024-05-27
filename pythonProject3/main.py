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
        conn.close()
        if (current_time - time).total_seconds() / 60 > 20 and current_time < delivery_time:
            return 1, id
        elif current_time > delivery_time:
            return 2, id
        elif (current_time - time).total_seconds() / 60 < 20:
            return 3, id
    except Exception:
        conn.close()
        return 0, 0


def print_main_menu():
    print('1. Register\n2. Login\nPress "h" for help')


def cancel_order(username):
    try:
        conn = sqlite3.connect('pizza_orders.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM orders WHERE username = ?''', (username,))
        order = c.fetchall()[-1]
        if get_order_status(username)[0] == 1 or get_order_status(username)[0] == 3:
            c.execute('''DELETE FROM orders WHERE id = ?''', (order[0],))
            print(f'The order {get_order_status(username)[1]} has been cancelled')
        else:
            print('There are no active orders')
        conn.commit()
        conn.close()
    except Exception:
        print('There are no active orders')


def select_option(username):
    while True:
        print('(1) Order Pizza')
        print('(2) Get history')
        print('(3) Get the order status')
        print('(4) Cancel the order')
        print('(5) Log out')
        option = input(': ')
        if option == '1':
            ordering(username)
        elif option == '2':
            get_order_history(username)
        elif option == '3':
            status = get_order_status(username)
            if status[0] == 1:
                print(f"The order {status[1]} is being delivered")
            elif status[0] == 2:
                print(f"The order {status[1]} is delivered")
            elif status[0] == 3:
                print(f"The order {status[1]} is being cooked")
            else:
                print('There are no orders')
        elif option == '4':
            cancel_order(username)
        elif option == '5':
            break


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

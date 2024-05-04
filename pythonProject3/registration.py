import sqlite3
import hashlib


def create_users_table():
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username text, hashed_password text, 
    rights text, preferences text)''')
    conn.commit()
    conn.close()


def check_username(username):
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''SELECT username FROM users WHERE username = ?''', (username,))
    result = c.fetchone()
    if result is not None:
        print('The nickname is busy, try another')
        return False
    return True


def add_user_to_database(username, hashed_password, rights, preferences):
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users VALUES (?, ?, ?, ?)''', (username, hashed_password, rights, preferences))
    conn.commit()
    conn.close()


def choose_preferences():
    print("Type in your desired ingredients separated by space: ")
    preferences = ', '.join(input().split())
    return preferences


def registration():
    create_users_table()
    username = input('Enter username: ')
    while not check_username(username):
        username = input('Enter username: ')
    password = input('Enter password: ')
    preferences = choose_preferences()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    create_users_table()  # Create the database if not already exist
    add_user_to_database(username, hashed_password, 'basic', preferences)
    print('User registered successfully!')
    return username


import sqlite3
from datetime import datetime, timedelta


def create_pizzas_table():
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    try:
        c.execute('''SELECT * FROM pizzas''')
    except sqlite3.OperationalError:
        c.execute('''CREATE TABLE IF NOT EXISTS pizzas (title text, ingredients text, cost int)''')
        c.execute('''INSERT INTO pizzas VALUES ("margarita", "tomato sauce, mozzarella cheese, tomato, basil", 489), 
            ("pepperoni", "cheese, salami, ham, onion, hot pepper", 429)''')
    conn.commit()
    conn.close()


def choose_time(time):
    while True:
        current_time = time
        time1 = current_time + timedelta(minutes=30)
        time2 = current_time + timedelta(hours=1)
        time3 = current_time + timedelta(hours=2)

        print(f"Choose delivery time: \n1. {time1.strftime('%H:%M')}\n2. {time2.strftime('%H:%M')}\n"
              f"3. {time3.strftime('%H:%M')}\nPress ENTER to type in your time")
        delivery_time = input()
        if delivery_time == '':
            while True:
                try:
                    print("Type in desired delivery time (hours:minutes): ")
                    temp = input()
                    delivery_time = current_time.replace(hour=int(temp.split(':')[0]), minute=int(temp.split(':')[1]))
                    if delivery_time <= current_time:
                        print('Incorrect delivery time. Try again')
                    elif delivery_time.replace(second=0) <= current_time.replace(second=0) + timedelta(minutes=30):
                        print('We wil not be able to deliver the pizza in that time. Type in a later time')
                    else:
                        return delivery_time
                except Exception:
                    print("Incorrect input. Try again")
        else:
            if delivery_time == '1':
                return time1
            elif delivery_time == '2':
                return time2
            elif delivery_time == '3':
                return time3
            else:
                print('Incorrect input')


def ordering(username):
    create_pizzas_table()
    basket = ['', 'Pepperoni', 'Margarita', 'Love']
    print('(1) - Pepperoni')
    print('(2) - Margarita')
    print('(3) - Love')
    print('To choose the desired ingredients press ENTER')
    order = list(map(int, input(': ').split()))
    quantity = 1
    if order:
        pizza_ordered = basket[order[0]]
    else:
        pizza_ordered = ''
    if len(order) > 1:
        quantity = order[1]
    if pizza_ordered == '':
        print("Type in your desired ingredients separated by space: ")
        ingredients = input().split()
        conn = sqlite3.connect('pizza_orders.db')
        c = conn.cursor()
        result = set()
        for ingredient in ingredients:
            c.execute('''SELECT title FROM pizzas WHERE ingredients LIKE "%"||?||"%"''', (ingredient,))
            pizzas = c.fetchall()
            for i in pizzas:
                result.add(i[0])
        if len(result) > 0:
            print("You would try these pizzas:", ', '.join([i for i in result]))
        else:
            print("Sorry, we have no pizza that satisfies your desires")

    else:
        conn = sqlite3.connect('pizza_orders.db')
        c = conn.cursor()
        c.execute('''SELECT cost FROM pizzas WHERE title = ?''', (pizza_ordered.lower(),))
        price = c.fetchone()[0]
        time = datetime.now().replace(microsecond=0)
        delivery_time = choose_time(time)
        add_order_to_database(username, pizza_ordered, quantity, time, delivery_time, price)
        print("Add ingredients")


def add_order_to_database(username, pizza_ordered, quantity, time, delivery_time, price):
    cost = calculate_cost(quantity, price)

    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)''',
              (username, pizza_ordered, quantity, str(time), str(delivery_time), cost))
    conn.commit()
    conn.close()
    print('Order added to the database successfully!')


# Function to calculate the cost of the order
def calculate_cost(quantity, price):
    # Add your own logic here to calculate the cost based on pizza and quantity
    cost = quantity * price
    return cost

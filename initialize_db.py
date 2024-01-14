import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('example.db')
c = conn.cursor()

# EXISTING ORDERS
# Create table
c.execute('''CREATE TABLE orders
             (id INTEGER PRIMARY KEY, order_date, delivery_time_min, status, client_phone)''')

# data to be added
orders = [
    (1, datetime.now() - timedelta(minutes=40), 60, 'В обработке', '1111'),
    (2, datetime.now() - timedelta(minutes=50), 50, 'Доставлен', '2222'),
    (3, datetime.now() - timedelta(minutes=20), 40, 'Готовится', '3333'),
    ]

# add data
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?)', orders)


# AVAILABLE INVENTORY
# Create table
c.execute('''CREATE TABLE menu
             (id INTEGER PRIMARY KEY, name, price)''')

# data to be added
menu = [
    (1, 'Пицца Маргарита', 550),
    (2, 'Спагетти Болоньезе', 450),
    (3, 'Салат Цезарь', 450),
    (4, 'Пицца 4 сыра', 200),
    (5, 'Карбонара', 300),
    (6, 'Крабовый салат', 450),
    (7, 'Огурцы', 1000),
    (8, 'Помидоры', 500),
    (9, 'Суп Куриный', 250),
    ]

# add data
c.executemany('INSERT INTO menu VALUES (?,?,?)', menu)


# SPECIAL OFFERS
# Create table
c.execute('''CREATE TABLE special_offers
             (id INTEGER PRIMARY KEY, text)''')

# data to be added
special_offers = [
    (1, 'Бесплатная доставка при заказе от $20'),
    (2, '10% скидка на все пиццы в понедельник')
    ]

# add data
c.executemany('INSERT INTO special_offers VALUES (?,?)', special_offers)

c.execute('''CREATE TABLE tables (id INTEGER PRIMARY KEY, text)''')

tables = [
    (1, 'Забронирован'),
    (2, 'Забронирован'),
    (3, 'Свободен')
]

c.executemany('INSERT INTO tables VALUES (?,?)', tables)

# Save (commit) the changes
conn.commit()

# end connection
conn.close()

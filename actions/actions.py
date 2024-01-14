from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from datetime import datetime


class ActionBookTable(Action):
    def name(self) -> Text:
        return "action_book_table"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(f"SELECT id FROM tables WHERE text='Свободен'").fetchall()
            if len(res) == 0:
                dispatcher.utter_message(text="Свободных столиков нет!")
            else:
                id = res[0][0]
                cursor.execute(f"UPDATE tables SET text='Забронирован' WHERE id={id};")    
                dispatcher.utter_message(text=f"Столик {id} успешно забронирован!")
        return []


class ActionOrderFood(Action):
    def name(self) -> Text:
        return "action_order_food"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        numbers_list = tracker.get_slot('numbers_list')
        phone_number = tracker.get_slot('phone')
        try:
            numbers_list = tuple(map(int, numbers_list))
        except:
            dispatcher.utter_message(text="Ошибка. Попробуйте спросить ещё раз")
        else:
            dispatcher.utter_message(text="Ваш заказ принят! Позиции по заказу:")
            with sqlite3.connect('example.db') as conn:
                cursor = conn.cursor()
                # Сохраняем заказ в таблицу orders
                order = [(datetime.now(), 60, 'В обработке', phone_number)]
                cursor.executemany('INSERT INTO orders (order_date, delivery_time_min, \
                                   status, client_phone) VALUES (?,?,?,?)', order)
                id = cursor.execute(f"SELECT id FROM orders WHERE id=(SELECT max(id) FROM orders)").fetchall()
                # Получаем наименования и цены по позициям
                res = cursor.execute(f"SELECT * FROM menu WHERE id IN {numbers_list};").fetchall()
                conn.commit()
            price = 0
            for row in res:
                text = f"{row[0]}. {row[1]} \t {row[2]} $"
                price += int(row[2])
                dispatcher.utter_message(text=text)
            dispatcher.utter_message(text=f"Общая сумма заказа: {price} $")
            dispatcher.utter_message(text=f"Спасибо за заказ! Номер вашего заказа {id[0][0]}. Ожидайте доставку.")
        return []


class ActionGetMenu(Action):
    def name(self) -> Text:
        return "action_get_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Вот наше меню:")
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute("SELECT * FROM menu;")
            for row in res.fetchall():
                text = f"{row[0]}. {row[1]} \t {row[2]} $"
                dispatcher.utter_message(text=text)
        return []


class ActionGetSpecialOffers(Action):
    def name(self) -> Text:
        return "action_get_special_offers"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="У нас есть следующие специальные предложения:")
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute("SELECT * FROM special_offers;")
            for row in res.fetchall():
                text = f"{row[0]}. {row[1]}"
                dispatcher.utter_message(text=text)
        return []


class ActionGetOrderStatus(Action):
    def name(self) -> Text:
        return "action_get_order_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot('order_id')
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            orders = cursor.execute(f"SELECT * FROM orders WHERE id={order_id};") \
                .fetchall()
        if orders:
            order_date = orders[0][1]
            delivery_time_min = orders[0][2]
            status = orders[0][3]

            message = f"Статус вашего заказа: {status} \nВремя доставки: {delivery_time_min} мин."
            message += f"\nДата и время заказа: {order_date.split('.')[0]}"
        else:
            message = "Заказ не найден"
        dispatcher.utter_message(text=message)
        return []

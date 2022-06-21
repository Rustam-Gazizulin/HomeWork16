from app import db
from models import User, Order, Offer
import data
import datetime


db.drop_all()
db.create_all()

for user in data.USERS:
    """Добавление данных в модель User"""

    db.session.add(User(
        id=user["id"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"],
        role=user["role"],
        phone=user["phone"]
    ))

    db.session.commit()

for order in data.ORDERS:
    """Добавление данных в модель Order"""

    data_time_obj_start = datetime.datetime.strptime(order["start_date"], '%m/%d/%Y')  # Конвертируем строку
    data_time_obj_end = datetime.datetime.strptime(order["end_date"], '%m/%d/%Y')  # в формат date

    db.session.add(Order(
        id=order["id"],
        name=order["name"],
        description=order["description"],
        start_date=data_time_obj_start.date(),
        end_date=data_time_obj_end,
        address=order["address"],
        price=order["price"],
        customer_id=order["customer_id"],
        executor_id=order["executor_id"]
    ))

    db.session.commit()

for offer in data.OFFERS:
    """Добавление данных в модель Offer"""

    db.session.add(Offer(
        id=offer["id"],
        order_id=offer["order_id"],
        executor_id=offer["executor_id"]
    ))

    db.session.commit()

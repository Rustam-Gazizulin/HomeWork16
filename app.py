import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import data

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False

db = SQLAlchemy(app)


class User(db.Model):
    """Модель User описывает данные о пользователе полученные из массива
     данных JSON в файле data, которые будут храниться в таблице"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Order(db.Model):
    """Модель Order описывает данные о заказе полученные из массива
    данных JSON в файле data, которые будут храниться в таблице"""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(100))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Offer(db.Model):
    """Модель Offer описывает данные о пользователях и принятых заказов, полученные из массива
    данных JSON в файле data, которые будут храниться в таблице"""

    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


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


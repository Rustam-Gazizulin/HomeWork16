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
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_data = db.Column(db.Date)
    end_data = db.Column(db.Date)
    address = db.Column(db.String(100))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


db.drop_all()
db.create_all()

for user in data.USERS:
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
    db.session.close()
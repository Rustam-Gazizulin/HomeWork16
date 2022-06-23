import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

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

    def create_dict(self):
        """Вспомогательный метод для конвертации полученных данных в словарь"""

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


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

    def create_dict(self):
        """Вспомогательный метод для конвертации полученных данных в словарь"""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    """Модель Offer описывает данные о пользователях и принятых заказов, полученные из массива
    данных JSON в файле data, которые будут храниться в таблице"""

    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def create_dict(self):
        """Вспомогательный метод для конвертации полученных данных в словарь"""

        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


@app.route("/users", methods=['GET', 'POST'])
def get_users():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех пользователей /users"""

    if request.method == 'GET':
        return jsonify([user.create_dict() for user in User.query.all()])
    if request.method == 'POST':
        try:
            user = json.loads(request.data)
            new_user_obj = User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            )
        except Exception as e:
            return e
        db.session.add(new_user_obj)
        db.session.commit()
        db.session.close()
        return 'Пользователь создан и добавлен в базу данных', 200


@app.route("/users/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_user_qid(qid: int):
    """Получение одного пользователя по идентификатору /users/1."""

    if request.method == 'GET':
        user_qid = User.query.get(qid)
        if user_qid is None:
            return 'User not found', 404
        return jsonify(User.create_dict(user_qid))
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user_qid = User.query.get(qid)
        if user_qid is None:
            return 'User not found', 404
        user_qid.first_name = user_data['first_name']
        user_qid.last_name = user_data['last_name']
        user_qid.age = user_data['age']
        user_qid.email = user_data['email']
        user_qid.role = user_data['role']
        user_qid.phone = user_data['phone']

        db.session.add(user_qid)
        db.session.commit()
        db.session.close()
        return f'Данные пользователя с id {qid} изменены', 200

    elif request.method == 'DELETE':
        user_qid = User.query.get(qid)
        if user_qid is None:
            return 'User not found', 404
        db.session.delete(user_qid)
        db.session.commit()
        db.session.close()

        return f'Данные пользователя с id {qid} удалены', 200


@app.route("/offers", methods=['GET', 'POST'])
def get_offers():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех offers"""

    if request.method == 'GET':
        return jsonify([offer.create_dict() for offer in Offer.query.all()])
    if request.method == 'POST':
        try:
            offer = json.loads(request.data)
            new_offer_obj = Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            )
        except Exception as e:
            return e
        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return 'Оффер создан и добавлен в базу данных', 200


@app.route("/offers/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_offer_qid(qid: int):
    """Получение одного offer по идентификатору /offers/qid."""
    if request.method == 'GET':
        offer_qid = Offer.query.get(qid)
        if offer_qid is None:
            return 'Offer not found'
        return jsonify(Offer.create_dict(offer_qid))

    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer_qid = Offer.query.get(qid)
        if offer_qid is None:
            return 'Offer not found', 404
        offer_qid.id = offer_data['id']
        offer_qid.order_id = offer_data['order_id']
        offer_qid.executor_id = offer_data['executor_id']

        db.session.add(offer_qid)
        db.session.commit()
        db.session.close()
        return f'Данные офера с id {qid} изменены', 200

    elif request.method == 'DELETE':
        offer_qid = Offer.query.get(qid)
        if offer_qid is None:
            return 'User not found', 404
        db.session.delete(offer_qid)
        db.session.commit()
        db.session.close()

        return f'Данные офера с id {qid} удалены', 200


@app.route("/orders", methods=['GET', 'POST'])
def get_orders():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех orders"""

    if request.method == 'GET':
        return jsonify([order.create_dict() for order in Order.query.all()])
    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = [int(i) for i in order['start_date'].split("/")]  # Конвертируем строку
            month_end, day_end, year_end = [int(i) for i in order['start_date'].split("/")]  # Конвертируем строку

            new_order_obj = Order(
                id=order["id"],
                name=order["name"],
                description=order["description"],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=year_end, month=month_end, day=day_end),
                address=order["address"],
                price=order["price"],
                customer_id=order["customer_id"],
                executor_id=order["executor_id"]
            )
            db.session.add(new_order_obj)
            db.session.commit()
            db.session.close()
            return 'Ордер создан и добавлен в базу данных', 200
        except Exception as e:
            return e


@app.route("/orders/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_order_qid(qid: int):
    """Получение одного order по идентификатору /orders/qid."""

    order_qid = Order.query.get(qid)
    if order_qid is None:
        return 'Order not found'
    return jsonify(Order.create_dict(order_qid))


if __name__ == '__main__':
    app.run()

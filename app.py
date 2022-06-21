from flask_sqlalchemy import SQLAlchemy
from datetime import date
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


@app.route("/users/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_user_qid(qid: int):
    """Получение одного пользователя по идентификатору /users/1."""

    user_qid = User.query.get(qid)
    if user_qid is None:
        return 'User not found'
    return jsonify(User.create_dict(user_qid))


@app.route("/offers", methods=['GET', 'POST'])
def get_offers():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех offers"""

    if request.method == 'GET':
        return jsonify([offer.create_dict() for offer in Offer.query.all()])


@app.route("/offers/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_offer_qid(qid: int):
    """Получение одного offer по идентификатору /offers/qid."""

    offer_qid = Offer.query.get(qid)
    if offer_qid is None:
        return 'Offer not found'
    return jsonify(Offer.create_dict(offer_qid))


@app.route("/orders", methods=['GET', 'POST'])
def get_orders():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех orders"""

    if request.method == 'GET':
        return jsonify([order.create_dict() for order in Order.query.all()])


@app.route("/orders/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_order_qid(qid: int):
    """Получение одного order по идентификатору /orders/qid."""

    order_qid = Order.query.get(qid)
    if order_qid is None:
        return 'Order not found'
    return jsonify(Order.create_dict(order_qid))


if __name__ == '__main__':
    app.run()

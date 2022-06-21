from flask_sqlalchemy import SQLAlchemy
import models
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False

db = SQLAlchemy(app)



@app.route("/users", methods=['GET', 'POST'])
def get_users():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех пользователей /users"""

    if request.method == 'GET':
        return jsonify([user.create_dict() for user in models.User.query.all()])


@app.route("/users/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_user_qid(qid: int):
    """Получение одного пользователя по идентификатору /users/1."""

    user_qid = models.User.query.get(qid)
    if user_qid is None:
        return 'User not found'
    return jsonify(models.User.create_dict(user_qid))


@app.route("/offers", methods=['GET', 'POST'])
def get_offers():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех offers"""

    if request.method == 'GET':
        return jsonify([offer.create_dict() for offer in models.Offer.query.all()])


@app.route("/offers/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_offer_qid(qid: int):
    """Получение одного offer по идентификатору /offers/qid."""

    offer_qid = models.Offer.query.get(qid)
    if offer_qid is None:
        return 'Offer not found'
    return jsonify(models.Offer.create_dict(offer_qid))


@app.route("/orders", methods=['GET', 'POST'])
def get_orders():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех orders"""

    if request.method == 'GET':
        return jsonify([order.create_dict() for order in models.Order.query.all()])


@app.route("/orders/<int:qid>", methods=['GET', 'PUT', 'DELETE'])
def get_order_qid(qid: int):
    """Получение одного order по идентификатору /orders/qid."""

    order_qid = models.Order.query.get(qid)
    if order_qid is None:
        return 'Order not found'
    return jsonify(models.Order.create_dict(order_qid))


if __name__ == '__main__':
    app.run()

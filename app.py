import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import models

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False

db = SQLAlchemy(app)


@app.route("/users", methods=['GET', 'POST'])
def get_users():
    """Представление для пользователей, которое обрабатывает GET-запросы получения всех пользователей users
     и одного пользователя по идентификатору /users/1."""

    if request.method == 'GET':
        return jsonify([user.create_dict() for user in models.User.query.all()])





if __name__ == '__main__':
    app.run()

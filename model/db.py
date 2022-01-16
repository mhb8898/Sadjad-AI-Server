from flask_sqlalchemy import SQLAlchemy
import jsonpickle
import sqlalchemy.types as types
from flask import Flask

app = Flask(__name__)

db = SQLAlchemy(app)


class JsonType(types.MutableType, types.TypeDecorator):
    impl = types.Unicode

    def process_bind_param(self, value, engine):
        return unicode(jsonpickle.encode(value))

    def process_result_value(self, value, engine):
        if value:
            return jsonpickle.decode(value)
        # default can also be a list
        return {}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(80), unique=True)
    student_num = db.Column(db.Integer, unique=True)

    def __init__(self, name, num):
        self.student_name = name
        self.student_num = num

    def __repr__(self):
        return '<User %r>' % self.student_name

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map= db.Column(JsonType)

class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    board_id=db.Column(db.Integer, db.ForeignKey(Board.id), primary_key=True)
    user=db.relationship('User', foreign_keys='Move.user_id')
    board=db.relationship('Board', foreign_keys='Move.board_id')
    x=db.Column(db.Integer)
    y=db.Column(db.Integer)

from concurrent.futures.process import _python_exit
import email
import json

from sqlalchemy import values
from app import db
from app import app
# import enum
# from app import security as scr


class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120))
    role = db.Column(db.String(120))
    realid = db.Column(db.Integer)
    passwordHash = db.Column(db.String(120))


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    passwordHash = db.Column(db.String(120))
    idea = db.relationship('Idea', backref='client', lazy='dynamic')
    todo = db.relationship('Todo', backref='client', lazy='dynamic')
    inprocess = db.relationship('Inprocess', backref='client', lazy='dynamic')
    done = db.relationship('Done', backref='client', lazy='dynamic')

    def toDict(self):
        dictionary = {}
        dictionary['idea'] = (list(
            map(lambda x: x.toDict(), self.idea)))
        dictionary['todo'] = (list(
            map(lambda x: x.toDict(), self.todo)))
        dictionary['inprocess'] = (list(
            map(lambda x: x.toDict(), self.inprocess)))
        dictionary['done'] = (list(
            map(lambda x: x.toDict(), self.done)))
        return dictionary


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    time = db.Column(db.String(120))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def toDict(self):
        dictionary = {}
        dictionary['name'] = self.name
        dictionary['description'] = self.description
        dictionary['date'] = self.time
        return dictionary


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    time = db.Column(db.String(120))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def toDict(self):
        dictionary = {}
        dictionary['name'] = self.name
        dictionary['description'] = self.description
        dictionary['date'] = self.time
        return dictionary


class Inprocess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    time = db.Column(db.String(120))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def toDict(self):
        dictionary = {}
        dictionary['name'] = self.name
        dictionary['description'] = self.description
        dictionary['date'] = self.time
        return dictionary


class Done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    time = db.Column(db.String(120))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def toDict(self):
        dictionary = {}
        dictionary['name'] = self.name
        dictionary['description'] = self.description
        dictionary['date'] = self.time
        return dictionary

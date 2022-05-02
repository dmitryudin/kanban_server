from app import db
import enum
from app import security as scr


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class CoffeHouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120))
    phone = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(120))
    rating = db.Column(db.Float)
    photos = db.relationship('photo', backref='coffehouse', lazy='dynamic')
    orders = db.relationship('order', backref='coffehouse', lazy='dynamic')
    coffes = db.relationship('coffe', backref='coffehouse', lazy='dynamic')


class Coffe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.relationship('photo', backref='coffehouse', lazy='dynamic')


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    backrefCoffes = db.Column(db.Integer, db.ForeignKey('coffe.id'))
    backrefCoffeHouse = db.Column(db.Integer, db.ForeignKey('coffehouse.id'))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    backrefCoffeHouse = db.Column(db.Integer, db.ForeignKey('coffehouse.id'))
    backrefClient = db.Column(db.Integer, db.ForeignKey('client.id'))

from app import app
from flask import request
import json
from app import model, db
from app import security as scr
import datetime
from flask import jsonify


def auth(func):  # TODO
    def is_auth():
        d = json.loads(request.get_data().decode('utf-8'))
        if True:
            return func()
        else:
            return 'not auth'
    return is_auth


@app.route('/client/registration', methods=['GET', 'POST'])
def clientRegistration():
    d = json.loads(request.get_data().decode('utf-8'))
    # создание пользователя
    user_obj = model.Client()
    user_obj.setData(d)
    user_obj.token = scr.generateToken(18)
    user_obj.dateOfRegistration = datetime.datetime.now().date()
    db.session.add(user_obj)
    db.session.commit()
    user_obj = model.Client.query.filter(
        model.Client.phone == d['phone']).first()
    user_obj.qr = scr.makeQrCode(user_obj.id)
    passport_obj = model.Passport()
    passport_obj.setData(d['_passport'])
    passport_obj.client = user_obj.id
    db.session.add(user_obj)
    db.session.add(passport_obj)
    db.session.commit()
    user_obj = model.Client.query.get(user_obj.id)
    return jsonify({"status": "ok"})


@app.route('/client/login',  methods=['GET', 'POST'])
def clientLogin():
    d = json.loads(request.get_data().decode('utf-8'))
    user_obj = model.Client.query.filter(
        model.Client.phone == d['login']).first()
    if scr.checkPasswordHash(d['password'], user_obj.passwordHash):
        return(jsonify({"status": "ok", "token": user_obj.token, "id": user_obj.id}))
    else:
        return(jsonify({"status": "failure"}))


@app.route('/client/edit_profile')
@auth
def clientEditProfile():
    return 'Hello World!'


@app.route('/client/test', methods=['GET', 'POST'])
def clientEditProfile():
    d = json.loads(request.get_data().decode('utf-8'))
    print(d['id'])
    return 'Hello World!'


@auth
@app.route('/client/getProfile', methods=['GET', 'POST'])
def clientGetProfile():
    d = json.loads(request.get_data().decode('utf-8'))
    print(d['id'])
    userObj = model.Client.query.get(int(d['id']))
    ret = userObj.getData()
    print(ret)
    return jsonify(ret)

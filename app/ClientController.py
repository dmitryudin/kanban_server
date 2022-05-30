from multiprocessing.connection import Client
from site import USER_BASE
from app import app
from flask import request
import json
from app import model, db
from app import security
import datetime
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token, jwt_required, get_jwt_identity
)


@cross_origin()
@app.route('/registration', methods=['GET', 'POST'])
def clientRegistration():
    d = json.loads(request.get_data().decode('utf-8'))
    if (model.Auth.query.filter_by(phone=d['login']).first() != None):
        return jsonify({"status": "phone exist"})
    if (model.Auth.query.filter_by(email=d['login']).first() != None):
        return jsonify({"status": "email exist"})
    auth = model.Auth()
    auth.phone = d['login']
    hash = security.generatePasswordHash(d['password'])
    auth.passwordHash = hash
    auth.role = 'client'
    userObj = model.Client()
    userObj.passwordHash = hash
    db.session.add(userObj)
    db.session.commit()
    db.session.refresh(userObj)
    auth.realid = userObj.id
    print(userObj.id)
    db.session.add(auth)
    db.session.commit()
    return jsonify({"status": "ok"})


@cross_origin()
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    d = json.loads(request.get_data().decode('utf-8'))
    phone = model.Auth.query.filter_by(phone=d['login']).first()
    email = model.Auth.query.filter_by(email=d['login']).first()
    entity = None
    if phone != None:
        entity = phone
    if email != None:
        entity = email
    if entity == None:
        return jsonify({"status": "None"})
    if entity != None:
        if security.checkPasswordHash(d['password'], entity.passwordHash):
            access_token = create_access_token(identity=entity.id, fresh=True)
            refresh_token = create_refresh_token(entity.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200


@cross_origin()
@app.route('/update', methods=['GET', 'POST'])
@jwt_required()
def update():
    d = json.loads(request.get_data().decode('utf-8'))
    userId = model.Auth.query.get(get_jwt_identity()).realid
    client = model.Client.query.get(userId)
    for task in client.idea:
        db.session.delete(task)
    for task in client.todo:
        db.session.delete(task)
    for task in client.inprocess:
        db.session.delete(task)
    for task in client.done:
        db.session.delete(task)
    for task in d['idea']:
        temptask = model.Idea()
        temptask.client_id = userId
        temptask.description = task['description']
        temptask.name = task['name']
        temptask.time = task['date']
        db.session.add(temptask)
    for task in d['todo']:
        temptask = model.Todo()
        temptask.client_id = userId
        temptask.description = task['description']
        temptask.name = task['name']
        temptask.time = task['date']
        db.session.add(temptask)
    for task in d['inprocess']:
        temptask = model.Inprocess()
        temptask.client_id = userId
        temptask.description = task['description']
        temptask.name = task['name']
        temptask.time = task['date']
        db.session.add(temptask)
    for task in d['done']:
        temptask = model.Done()
        temptask.client_id = userId
        temptask.description = task['description']
        temptask.name = task['name']
        temptask.time = task['date']
        db.session.add(temptask)
    db.session.commit()
    return jsonify({"status": "ok"})


@cross_origin()
@app.route('/get_data', methods=['GET', 'POST'])
@jwt_required()
def get_data():
    userId = model.Auth.query.get(get_jwt_identity()).realid
    client = model.Client.query.get(userId)
    print('json')
    print(client.toDict())
    return jsonify(client.toDict())

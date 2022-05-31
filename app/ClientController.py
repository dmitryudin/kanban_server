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


@app.route('/registration', methods=['GET', 'POST'])
@cross_origin()
def clientRegistration():
    d = json.loads(request.get_data().decode('utf-8'))
    print(d['login'])
    print(model.Auth.query.filter_by(login=d['login']).first())
    if (model.Auth.query.filter_by(login=d['login']).first() != None):
        return jsonify({"status": "user exist"}), 409
    auth = model.Auth()
    auth.login = d['login']
    hash = security.generatePasswordHash(d['password'])
    auth.passwordHash = hash
    auth.role = d['role']
    userObj = model.Client()
    userObj.passwordHash = hash
    db.session.add(userObj)
    db.session.commit()
    db.session.refresh(userObj)
    auth.realid = userObj.id
    print(userObj.id)
    db.session.add(auth)
    db.session.commit()
    return jsonify({"status": "ok"}), 201


@app.route('/auth', methods=['GET', 'POST'])
@cross_origin()
def auth():
    print('Auth!', request.authorization.username)
    print('Auth!', request.authorization.password)
    auth = model.Auth.query.filter_by(
        login=request.authorization.username).first()
    if auth == None:
        return {'status': 'user is not exist'}, 404
    if auth != None:
        if security.checkPasswordHash(request.authorization.password, auth.passwordHash):
            access_token = create_access_token(identity=auth.id, fresh=True)
            refresh_token = create_refresh_token(auth.id)
            return {
                'lifetime': app.config['TOKENS_LIFETIME'],
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200


@app.route('/refresh', methods=['GET', 'POST'])
@jwt_required(refresh=True)
@cross_origin()
def refreshAccessToken():
    # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
    print('sdfsdf')
    current_user = get_jwt_identity()
    # return a non-fresh token for the user
    new_token = create_access_token(identity=current_user, fresh=False)
    return {'access_token': new_token}, 200


@app.route('/update', methods=['GET', 'POST'])
# @cross_origin()
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


@app.route('/get_data', methods=['GET', 'POST'])
# @cross_origin()
@jwt_required(fresh=True)
def get_data():

    userId = model.Auth.query.get(get_jwt_identity()).realid
    client = model.Client.query.get(userId)
    print('userId', userId)
    print('json')
    print(client.toDict())
    return jsonify(client.toDict())

    return {}

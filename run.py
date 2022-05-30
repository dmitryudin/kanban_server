import threading
from app import app
from flask_jwt_extended import JWTManager
#from flask_socketio import SocketIO
app.config['CORS_HEADERS'] = 'Content-Type'
#socketio = SocketIO(app)
app.config['JWT_SECRET_KEY'] = 'this-is-super-secret'
jwt = JWTManager(app)
app.run(debug=True, host='2.59.41.249', port=3030)
#socketio.run(app, debug=True, host='2.59.41.249', port=5050, )

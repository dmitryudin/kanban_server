from app import app
from flask_socketio import SocketIO

socketio = SocketIO(app)
#app.run(debug=True, host='localhost', port=5050)
socketio.run(app, debug=True, host='2.59.41.249', port=5050)

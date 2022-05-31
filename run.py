import threading
from app import app
from flask_jwt_extended import JWTManager
from datetime import timedelta
# from flask_socketio import SocketIO
app.config['CORS_HEADERS'] = 'Content-Type'
# socketio = SocketIO(app)
app.config['JWT_SECRET_KEY'] = 'this-is-super-secret'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['TOKENS_LIFETIME'] = 3400  # 5*60
jwt = JWTManager(app)
app.run(debug=True, host='2.59.41.249', port=3030)
# socketio.run(app, debug=True, host='2.59.41.249', port=5050, )

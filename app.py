from flask import *
from backend.models.basic_model import *
# import requests
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object('backend.models.config')
db = db_setup(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

from backend.user.app import *
from backend.massage.app import *

if __name__ == '__main__':
    socketio.run(app, debug=True)

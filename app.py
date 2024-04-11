from flask import *
from backend.models.basic_model import *
# import requests
from flask_cors import CORS
from flask_migrate import Migrate
# from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
app.config.from_object('backend.models.config')
db = db_setup(app)

migrate = Migrate(app, db)
CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")
jwt = JWTManager(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


from backend.user.app import *
from backend.admin.app import *
from backend.massage.app import *
from backend.universities.main import *
from backend.security.token import *
from backend.tariff.register import *

if __name__ == '__main__':
    app.run()

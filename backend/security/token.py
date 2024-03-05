from app import *
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from backend.settings.settings import *


@app.route(f'{api}/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    user = User.query.filter_by(username=identity).first()
    return jsonify({
        'user': user.json(),
        'personal': user.personal_json(),
        'parents': user.student.json(),
        'access_token': access_token
    })



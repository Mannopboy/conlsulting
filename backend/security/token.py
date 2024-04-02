from app import request, app, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from backend.settings.settings import api, img_file, check_account_types, check_file_type, add_countries, admin, \
    check_payment, student_code
from backend.models.basic_model import url
from backend.models.basic_model import User
import random


@app.route(f'{api}/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    user = User.query.filter_by(username=identity).first()
    refresh_token = create_refresh_token(identity=user.id)
    user_img = None
    if user and user.files:
        for img in user.files:
            print(img.file_type_id)
            if img.file_type_id == 12:
                user_img = f'{url}{img.file}',
    print(user_img)
    if user.role == student_code:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'user_img': user_img,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'status': check_payment(user.id)
        })
    else:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'user_img': user_img,
            'access_token': access_token,
            'refresh_token': refresh_token
        })


@app.route(f'{api}/update_base/<string:password>')
def update_base(password):
    if password == 'nigga_1942':
        check_file_type()
        check_account_types()
        admin()
        add_countries()
        return jsonify({
            'status': 'Nigga'
        })
    else:
        bollen_list = ['True', 'False', 'None', 'Error', 'Ip error', 'TypeError', 'Token error']
        return jsonify({
            'status': random.choice(bollen_list)
        })

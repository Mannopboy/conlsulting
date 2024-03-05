from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from backend.settings.settings import *
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from backend.settings.settings import *


@app.route(f'{api}/check_username', methods=['POST'])
@jwt_required()
def check_username():
    username = request.get_json()['username']
    users = User.query.order_by(User.id).all()
    status = True
    for user in users:
        if user.username == username:
            status = False
        else:
            status = True
    return jsonify({
        'status': status
    })


@app.route(f'{api}/profile', methods=['POST'])
@jwt_required()
def profile():
    id = request.get_json()
    user = User.query.filter(User.id == id).first()
    file_type = FileType.query.order_by(FileType.id).all()
    all_country = Country.query.order_by(Country.id).all()
    list = []
    number = 0
    countries = []
    for country in all_country:
        countries.append(country.json())
    for type in file_type:
        if type.status and user:
            status = File.query.filter(File.file_type_id == type.id, File.user_id == user.id).first()
            if not status:
                status = False
            else:
                status = True
            info = {
                "value": status,
                'name': type.name,
                "order": number
            }
            list.append(info)
            number += 1
    if user:
        return jsonify({
            'status': True,
            'user': user.json(),
            'parents': user.student.json(),
            'files': list,
            'countries': countries
        })
    else:
        return jsonify({
            'status': False
        })


# @app.route('/change_parents', methods=['POST'])
# def change_parents():
#     req = request.get_json()
#     user_id = req['user_id']
#     name = req['name']
#     surname = req['surname']
#     email = req['email']
#     nationality = req['nationality']
#     number = req['number']
#     passport_number = req['passport_number']
#     date_birth = req['date_birth']
#     country_id = req['country_id']
#     address = req['address']
#     user = User.query.filter(User.id == user_id).first()
#     print(req)
#     user.name = name
#     user.country_id = country_id
#     user.surname = surname
#     user.email = email
#     user.nationality = nationality
#     user.number = number
#     user.passport_number = passport_number
#     user.date_birth = date_birth
#     user.address = address
#     db.session.commit()
#     list = []
#     all_country = Country.query.order_by(Country.id).all()
#     countries = []
#     for country in all_country:
#         countries.append(country.json())
#     return jsonify({
#         'status': True,
#         'user': user.json(),
#         'files': list,
#         'countries': countries
#     })


# @app.route('/change_user', methods=['POST'])
# def change_user():
#     req = request.get_json()
#     user_id = req['user_id']
#     name = req['name']
#     surname = req['surname']
#     email = req['email']
#     nationality = req['nationality']
#     number = req['number']
#     passport_number = req['passport_number']
#     date_birth = req['date_birth']
#     country_id = req['country_id']
#     address = req['address']
#     user = User.query.filter(User.id == user_id).first()
#     print(req)
#     user.name = name
#     user.country_id = country_id
#     user.surname = surname
#     user.email = email
#     user.nationality = nationality
#     user.number = number
#     user.passport_number = passport_number
#     user.date_birth = date_birth
#     user.address = address
#     db.session.commit()
#     list = []
#     all_country = Country.query.order_by(Country.id).all()
#     countries = []
#     for country in all_country:
#         countries.append(country.json())
#     return jsonify({
#         'status': True,
#         'user': user.json(),
#         'files': list,
#         'countries': countries
#     })


@app.route(f'{api}/register_img', methods=['POST'])
@jwt_required()
def register_img():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    file = request.files.get('img')
    type = req['type']
    user_id = req['id']
    file_type = FileType.query.filter(FileType.name == type).first()
    file_url = file_type.name
    user = User.query.filter(User.id == user_id).first()
    img = File.query.filter(File.user_id == user.id, File.file_type_id == file_type.id).first()
    if file:
        # img_name = f'{secure_filename(file.filename)}#/{random.randrange(1, 1000)}{file_type.id}/#'
        img_name = secure_filename(file.filename)
        app.config["UPLOAD_FOLDER"] = file_url
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
        img_url = file_url + img_name
        if not img:
            img = File(file=img_url, user_id=user.id, file_type_id=file_type.id)
            img.add()
            new_img = File.query.filter(File.user_id == user.id, File.file_type_id == file_type.id).first()
            img_url = new_img.json()['img']['value']
            return jsonify({
                'status': True,
                'img': img_url
            })
        else:
            if img.file != url:
                os.remove(img.file)
            img.file = url
            db.session.commit()
            img_url = img.json()['img']['value']
            return jsonify({
                'status': True,
                'img': img_url
            })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/register', methods=['POST'])
def register():
    req = request.get_json()
    name = req.get('name')
    surname = req.get('surname')
    username = req['username']
    password = req['password']
    role = '09df5vd0fv'
    number = req['number']
    date_birth = req['date']
    hashed = generate_password_hash(password=password)
    user = User.query.filter(User.username == username).first()
    if not user:
        user = User(username=username, password=hashed, name=name, surname=surname, role=role, number=number,
                    date_birth=date_birth)
        user.add()
        student = Student(user_id=user.id)
        student.add()
        user = User.query.filter(User.id == user.id).first()
        return jsonify({
            'status': True,
            'username': user.username,
            'role': user.role,
            'user_img': user.user_img
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/login', methods=['POST'])
def login():
    check_file_type()
    username = request.get_json()['username']
    password = request.get_json()['password']
    username_sign = User.query.filter_by(username=username).first()
    user_img = None
    if username_sign and username_sign.files:
        for img in username_sign.files:
            if img.file_type_id == 14:
                user_img = f'{url}/{img.file}',
            else:
                user_img = False
    if username_sign and check_password_hash(username_sign.password, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        session['username'] = username
        return jsonify({
            'id': username_sign.id,
            'username': username_sign.username,
            'role': username_sign.role,
            'user_img': user_img,
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/logout', methods=['POST'])
def logout():
    session['username'] = None
    return jsonify({
        'status': True
    })


@app.route(f'{api}/personal_information', methods=['POST'])
@jwt_required()
def personal_information():
    all_country = Country.query.order_by(Country.id).all()
    user_id = request.get_json()
    user = User.query.filter(User.id == user_id).first()
    countries = []
    for country in all_country:
        info = {
            'name': country.name,
            'id': country.id
        }
        countries.append(info)
    if user:
        return jsonify({
            'status': True,
            'countries': countries,
            'user': user.personal_json(),
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/parents_information', methods=['POST'])
@jwt_required()
def parents_information():
    all_country = Country.query.order_by(Country.id).all()
    check_file_type()
    user_id = request.get_json()
    user = User.query.filter(User.id == user_id).first()
    countries = []
    for country in all_country:
        info = {
            'name': country.name,
            'id': country.id
        }
        countries.append(info)
    if user:
        return jsonify({
            'status': True,
            'countries': countries,
            'user': user.student.json(),
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/change_personal_information', methods=['POST'])
@jwt_required()
def change_personal_information():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    user_id = req['id']
    name = req['name']
    surname = req['surname']
    passport_number = req['passport_number']
    address = req['address']
    date_birth = req['date_birth']
    country_id = req['place_of_birth']
    school_studied = req['school_studied']
    user = User.query.filter(User.id == user_id).first()
    user.name = name
    user.surname = surname
    country = Country.query.filter(Country.id == country_id).first()
    if country:
        user.country_id = country.id
    user.passport_number = passport_number
    if date_birth:
        if type(date_birth) != "<class 'function'>":
            user.date_birth = date_birth
    user.address = address
    user.school_studied = school_studied
    db.session.commit()
    file = request.files.get('img')
    if file:
        img = File.query.filter(File.user_id == user.id, File.file_type_id == 14).first()
        if not img:
            type_file = FileType.query.filter(FileType.id == 14).first()
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = img_file + type_file.name
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = f'{img_file}{type_file.name}/{img_name}'
            img = File(file=img_url, file_type_id=type_file.id, user_id=user.id)
            img.add()
        else:
            if img.file:
                os.remove(img.file)
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = img_file + img.file_type.name
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = f'{img_file}{img.type.name}/{img_name}'
            img.img = img_url
    else:
        return jsonify({
            'status': False,
            'user': user.personal_json()
        })
    return jsonify({
        'status': True,
        'user': user.personal_json(),
    })


@app.route(f'{api}/change_parents_information', methods=['POST'])
@jwt_required()
def change_parents_information():
    req = request.get_json()
    user_id = req['id']
    parent_name = req['parent_name']
    parent_surname = req['parent_surname']
    address_id = req['address']
    date_birth = req['date_birth']
    country_id = req['place_of_work']
    position = req['position']
    parent_phone_number = req['parent_phone_number']
    parent_passport_number = req['parent_passport_number']
    parent_passport_expiration = req['parent_passport_expiration']
    user = User.query.filter(User.id == user_id).first()
    student = user.student
    student.parent_name = parent_name
    student.parent_surname = parent_surname
    if address_id:
        student.country_of_address_id = address_id
    if date_birth:
        if type(date_birth) != "<class 'function'>":
            student.date_birth = date_birth
    if country_id:
        student.country_of_work_id = country_id
    student.position = position
    student.parent_phone_number = parent_phone_number
    student.parent_passport_number = parent_passport_number
    student.parent_passport_expiration = parent_passport_expiration
    db.session.commit()
    return jsonify({
        'status': True,
        'user': user.student.json()
    })


@app.route(f'{api}/portfolio', methods=['POST'])
@jwt_required()
def portfolio():
    user_id = request.get_json()
    user = User.query.filter(User.id == user_id).first()
    file_type = FileType.query.order_by(FileType.id).all()
    list = []
    number = 0
    for type in file_type:
        if type.status and user:
            status = File.query.filter(File.file_type_id == type.id, File.user_id == user.id).first()
            if not status:
                status = False
            else:
                status = True
            info = {
                "value": status,
                'name': type.name,
                "order": number
            }
            list.append(info)
            number += 1
    if user:
        return jsonify({
            'status': True,
            'list': list
        })


@app.route(f'{api}/change_portfolio', methods=['POST'])
@jwt_required()
def change_portfolio():
    user_id = request.form.get('id')
    files = request.files

    user = User.query.filter(User.id == user_id).first()
    for file in files:
        file_type = file
        file = request.files.get(file)
        file_type = FileType.query.filter(FileType.name == file_type).first()
        file_old = File.query.filter(File.user_id == user.id, File.file_type_id == file_type.id).first()
        if not file_old:
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = img_file + file_type.name
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = f'{img_file}{file_type.name}/{img_name}'
            img = File(file=img_url, file_type_id=file_type.id, user_id=user.id)
            img.add()
        else:
            if file_old.file:
                os.remove(file_old.file)
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = img_file + file_old.file_type.name
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = f'{img_file}{file_old.type.name}/{img_name}'
            file_old.img = img_url
    file_type = FileType.query.order_by(FileType.id).all()
    list = []
    number = 0
    for type in file_type:
        if type.status:
            status = File.query.filter(File.file_type_id == type.id, File.user_id == user.id).first()
            if not status:
                status = False
            else:
                status = True
            info = {
                "value": status,
                'name': type.name,
                "order": number
            }
            list.append(info)
            number += 1
    return jsonify({
        'status': True,
        'files': list
    })

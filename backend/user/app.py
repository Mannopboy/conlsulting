from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from backend.settings.settings import *
from werkzeug.utils import secure_filename
import os
import random


@app.route('/get_university')
def get_university():
    # country_id = request.get_json()['country_id']
    country_id = 236
    country = Country.query.filter(Country.id == country_id).first()
    country_class = CountryClass(country.name)
    return jsonify({
        'all_university': country_class.get_universities()
    })


@app.route('/check_username', methods=['POST'])
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

@app.route('/change_user', methods=['POST'])
def change_user():
    req = request.get_json()
    print(req)
    user_id = req['user_id']
    email = req['email']
    nationality = req['nationality']
    number = req['number']
    passport_number = req['passport_number']
    date_birth = req['date_birth']
    address = req['address']
    user = User.query.filter(User.id == user_id).first()
    user.email = email
    user.nationality = nationality
    user.number = number
    user.passport_number = passport_number
    user.date_birth = date_birth
    user.address = address
    db.session.commit()
    return jsonify({
        'status': True,
        'user': user.json(),
        'student': user.student.json()
    })


@app.route('/register_package', methods=['POST'])
def register_package():
    user = current_user()
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    type = req['type']
    title = req['title']
    textarea = req['textarea']
    tariff_id = req['id']
    tariff = Tariff.query.filter(Tariff.id == tariff_id).first()
    if type == 'package_img':
        file = request.files.get('img')
        if file:
            # img_name = f'{secure_filename(file.filename)}#/{random.randrange(1, 1000)}{tariff.id}/#'
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = package_img()
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = package_img() + img_name
            package = Package(name=title, text=textarea, tariff_id=tariff.id, img=img_url, status=True, deleted=False)
            package.add()
            return jsonify({
                'status': True,
                'package': package.json()
            })
        else:
            return jsonify({
                'status': False
            })
    else:
        link = req['videoLink']
        package = Package(name=title, text=textarea, tariff_id=tariff.id, link=link, status=False, deleted=False)
        package.add()
        return jsonify({
            'status': True,
            'package': package.json()
        })


@app.route('/register_img', methods=['POST'])
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


@app.route('/get_tariff')
def get_tariff():
    tariff_all = Tariff.query.order_by(Tariff.id).all()
    data = []
    for tariff in tariff_all:
        data.append(tariff.json())
    return jsonify({
        'status': True,
        'data': data,
    })


@app.route('/delete_package/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    package = Package.query.filter(Package.id == package_id).first()
    package.deleted = True
    db.session.commit()
    return jsonify({
        'status': True
    })


@app.route('/change_package', methods=['POST'])
def change_package():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    package_id = req['id']
    print(package_id)
    package = Package.query.filter(Package.id == package_id).first()
    name = req['title']
    textarea = req['textarea']
    status = req['status']
    package.name = name
    package.text = textarea
    if status == 'true':
        file = request.files.get('img')
        if file:
            if package.img:
                os.remove(package.img)
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = package_img()
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = package_img() + img_name
            package.img = img_url
            package.status = True
        else:
            return jsonify({
                'status': False
            })
    else:
        link = req['link']
        package.status = False
        package.link = link
    db.session.commit()
    return jsonify({
        'status': True,
        'package': package.json()
    })


@app.route('/get_package', methods=['POST'])
def get_package():
    id = request.get_json()
    tariff = Tariff.query.filter(Tariff.id == id).first()
    return jsonify({
        'status': True,
        'tariff': tariff.json(),
    })


@app.route('/register_tariff', methods=['POST'])
def register_tariff():
    req = request.get_json()
    print(req)
    name = req['name']
    cost = req['cost']
    color = req['color']
    additions = req['selectedSubs']
    tariff = Tariff.query.filter(Tariff.name == name).first()
    if not tariff:
        tariff = Tariff(name=name, color=color, cost=cost)
        tariff.add()
        for addition in additions:
            addition_tariff = AdditionTariff(first_tariff=tariff.id, second_tariff=addition)
            addition_tariff.add()
        return jsonify({
            'status': True,
            'tariff': tariff.json(),
        })
    else:
        return jsonify({
            'status': False
        })


@app.route('/register', methods=['POST'])
def register():
    req = request.get_json()
    name = req.get('name')
    surname = req.get('surname')
    username = req['username']
    password = req['password']
    role = 'student'
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


@app.route('/login', methods=['POST'])
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
        session['username'] = username
        return jsonify({
            'id': username_sign.id,
            'username': username_sign.username,
            'role': username_sign.role,
            'user_img': user_img
        })
    else:
        return jsonify({
            'status': False
        })


@app.route('/logout', methods=['POST'])
def logout():
    session['username'] = None
    return jsonify({
        'status': True
    })


@app.route('/profile', methods=['POST'])
def profile():
    id = request.get_json()
    user = User.query.filter(User.id == id).first()
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
    print(list)
    print(user.json())
    if user:
        return jsonify({
            'status': True,
            'user': user.json(),
            'parents': user.student.json(),
            'files': list
        })
    else:
        return jsonify({
            'status': False
        })


@app.route('/personal_information', methods=['POST'])
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


@app.route('/parents_information', methods=['POST'])
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


@app.route('/register_connect', methods=['POST'])
def register_connect():
    req = request.get_json()
    user_id = req['user_id']
    tariff_id = req['tariff_id']
    user = User.query.filter(User.id == user_id).first()
    tariff = Tariff.query.filter(Tariff.id == tariff_id).first()
    if user and tariff:
        new_connect = StudentConnectedTariff(student_id=user.student.id, tariff_id=tariff.id)
        new_connect.add()
        return jsonify({
            'status': True
        })
    else:
        return jsonify({
            'status': False
        })


@app.route('/change_personal_information', methods=['POST'])
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
    date_of_expiration = req['date_of_expiration']
    school_studied = req['school_studied']
    user = User.query.filter(User.id == user_id).first()
    user.name = name
    user.surname = surname
    country = Country.query.filter(Country.id == country_id).first()
    if country:
        user.country_id = country.id
    if date_of_expiration:
        print(type(date_of_expiration))
        if type(date_of_expiration) != "<class 'function'>":
            user.date_of_expiration = date_of_expiration
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


@app.route('/change_parents_information', methods=['POST'])
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


@app.route('/portfolio', methods=['POST'])
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


@app.route('/change_portfolio', methods=['POST'])
def change_portfolio():
    user_id = request.form.get('id')
    files = request.files
    print(files)
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

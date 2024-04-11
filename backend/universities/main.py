from app import request, jsonify, json, secure_filename, app, render_template
from flask_jwt_extended import jwt_required
from backend.settings.settings import *
from backend.models.basic_model import University, Country, Occupation, Images, UniversityOccupation


@app.route(f'{api}/get_universities', methods=['GET'])
@jwt_required()
def get_universities():
    university_all = University.query.order_by(University.id).all()
    list = []
    for university in university_all:
        list.append(university.json())
    return jsonify({
        'status': True,
        'list': list
    })


@app.route(f'{api}/get_occupations_in_university', methods=['POST'])
@jwt_required()
def get_occupations_in_university():
    university_id = request.get_json()
    occupations = UniversityOccupation.query.filter(UniversityOccupation.university_id == university_id).order_by(
        UniversityOccupation.id).all()
    list = []
    for occupation in occupations:
        list.append(occupation.occupation.json())
    return jsonify({
        'status': True,
        'list': list
    })


@app.route(f'{api}/get_universities_in_country', methods=['POST'])
@jwt_required()
def get_universities_in_country():
    country_id = request.get_json()
    university_all = University.query.filter(University.country_id == country_id).order_by(University.id).all()
    list = []
    for university in university_all:
        list.append(university.json())
    return jsonify({
        'status': True,
        'list': list
    })


@app.route(f'{api}/add_university', methods=['POST'])
@jwt_required()
def add_university():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    files = request.files

    list = []
    if 'image_1' in files:
        list.append(files['image_1'])
    if 'image_2' in files:
        list.append(files['image_2'])
    if 'image_3' in files:
        list.append(files['image_3'])
    if 'image_4' in files:
        list.append(files['image_4'])

    name = req['name']
    place = req['text']
    web_pages = req['web_pages']
    country_id = None
    for id in req['country_id']:
        country_id = id
    list_id = req['list_id']
    university = University.query.filter(University.name == name).first()
    if not university:
        university = University(name=name, place=place, web_pages=web_pages, country_id=country_id)
        university.add()
        for file in list:
            if file and checkFile(file.filename):
                img_name = secure_filename(file.filename)
                app.config["UPLOAD_FOLDER"] = img_file2 + 'country_img'
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
                img_url = f'{img_file}university_img/{img_name}'
                img = Images(img=img_url, university_id=university.id, file_type_id=17)
                img.add()
        for id in list_id:
            university_occupation = UniversityOccupation(university_id=university.id, occupation_id=id)
            university_occupation.add()
        return jsonify({
            'status': True,
            'university': university.json(),
            'text': Messages.register_university()
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/get_countries', methods=['GET'])
@jwt_required()
def get_countries():
    countries = Country.query.order_by(Country.id).all()
    list = []
    for country in countries:
        list.append(country.json())
    return jsonify({
        'status': True,
        'list': list
    })


@app.route(f'{api}/change_occupation', methods=['POST'])
@jwt_required()
def change_occupation():
    id = request.form.get('id')
    name = request.form.get('name')
    file = request.files.get('img')
    occupation = Occupation.query.filter(Occupation.id == id).first()
    if occupation:
        occupation.name = eval(name)
        if file:
            Images.query.filter(Images.occupation_id == id).delete()
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = img_file2 + 'university_img'
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = f'{img_file}university_img/{img_name}'
            img = Images(img=img_url, occupation_id=id, file_type_id=18)
            img.add()
        db.session.commit()
        return jsonify({
            'status': True,
            'text': Messages.change_occupation(),
            'occupation': occupation.json()
        })


@app.route(f'{api}/get_occupation', methods=['GET'])
@jwt_required()
def get_occupation():
    occupations = Occupation.query.order_by(Occupation.id).all()
    list = []
    for occupation in occupations:
        list.append(occupation.json())
    return jsonify({
        'status': True,
        'list': list
    })


@app.route(f'{api}/change_university', methods=['PUT'])
@jwt_required()
def change_university():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    files = request.files
    if 'list' in req:
        new_list = req['list']
    else:
        new_list = []
    list = []
    if 'image_1' in files:
        list.append(files['image_1'])
    if 'image_2' in files:
        list.append(files['image_2'])
    if 'image_3' in files:
        list.append(files['image_3'])
    if 'image_4' in files:
        list.append(files['image_4'])

    university_id = req['id']
    name = req['name']
    place = req['text']
    web_pages = req['web_pages']
    country_id = None
    for id in req['country_id']:
        country_id = id
    list_id = req['list_id']
    university = University.query.filter(University.id == university_id).first()
    if university:
        university.name = name
        university.place = place
        university.web_pages = web_pages
        university.country_id = country_id
        db.session.commit()
        university_occupations = UniversityOccupation.query.filter(
            UniversityOccupation.university_id == university.id).order_by(UniversityOccupation.id).all()
        for item in university_occupations:
            UniversityOccupation.query.filter(UniversityOccupation.id == item.id).delete()
            db.session.commit()
        for id in list_id:
            university_occupation = UniversityOccupation(university_id=university.id, occupation_id=id)
            university_occupation.add()
        for id in new_list:
            Images.query.filter(Images.id == id).delete()
            db.session.commit()
        for file in list:
            if file and checkFile(file.filename):
                img_name = secure_filename(file.filename)
                app.config["UPLOAD_FOLDER"] = img_file2 + 'university_img'
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
                img_url = f'{img_file}university_img/{img_name}'
                img = Images(img=img_url, university_id=university.id, file_type_id=17)
                img.add()

        return jsonify({
            'status': True,
            'university': university.json(),
            'text': Messages.register_university()
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/change_country', methods=['POST'])
@jwt_required()
def change_country():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    files = request.files
    id = req['id']
    name = req['name']

    if 'list' in req:
        new_list = req['list']
    else:
        new_list = []
    list = []
    if 'image_1' in files:
        list.append(files['image_1'])
    if 'image_2' in files:
        list.append(files['image_2'])
    if 'image_3' in files:
        list.append(files['image_3'])
    if 'image_4' in files:
        list.append(files['image_4'])
    if name:
        country = Country.query.filter(Country.id == id).first()
        for id in new_list:
            Images.query.filter(Images.id == id).delete()
            db.session.commit()
        for file in list:
            if file and checkFile(file.filename):
                img_name = secure_filename(file.filename)
                app.config["UPLOAD_FOLDER"] = img_file2 + 'country_img'
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
                img_url = f'{img_file}country_img/{img_name}'
                img = Images(img=img_url, country_id=country.id, file_type_id=17)
                img.add()

        country.name = name
        db.session.commit()
        return jsonify({
            'status': True,
            'country': country.json(),
            'text': Messages.change_country()
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/add_occupation', methods=['POST'])
@jwt_required()
def add_occupation():
    req = request.get_json()
    occupation_name = req['name']
    occupation = Occupation.query.filter(Occupation.name == occupation_name).first()
    if not occupation:
        occupation = Occupation(name=occupation_name)
        occupation.add()
        return jsonify({
            'status': True,
            'occupation': occupation.json(),
            'text': Messages.register_occupation()
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/register_img', methods=['POST'])
@jwt_required()
def register_img():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    file = request.files.get('img')
    type = req['type']
    id_f = req['id']
    file_type = FileType.query.filter(FileType.name == type).first()
    file_url = file_type.name
    if file_url == 'country_img':
        country = Country.query.filter(Country.id == id_f).first()
        university = None
        occupation = None
    elif file_url == 'university_img':
        university = University.query.filter(University.id == id_f).first()
        country = None
        occupation = None
    else:
        occupation = Occupation.query.filter(Occupation.id == id_f).first()
        university = None
        country = None

    if file and checkFile(file.filename):
        img_name = secure_filename(file.filename)
        app.config["UPLOAD_FOLDER"] = img_file2 + file_url
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
        img_url = f'{img_file}{file_url}/{img_name}'
        if file_url == 'country_img':
            img = Images(img=img_url, country_id=country.id, file_type_id=file_type.id)
            img.add()
            object = country.json()
        elif file_url == 'university_img':
            img = Images(img=img_url, university_id=university.id, file_type_id=file_type.id)
            img.add()
            object = university.json()
        else:
            img = Images(img=img_url, occupation_id=occupation.id, file_type_id=file_type.id)
            img.add()
            object = occupation.json()
        return jsonify({
            'status': True,
            'object': object,
            'text': Messages.register_img()
        })

    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/register_images', methods=['POST'])
@jwt_required()
def register_images():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    files = request.files.get('img')
    type = req['type']
    id_f = req['id']
    file_type = FileType.query.filter(FileType.name == type).first()
    file_url = file_type.name
    if file_url == 'country_img':
        country = Country.query.filter(Country.id == id_f).first()
        university = None
        occupation = None
    elif file_url == 'university_img':
        university = University.query.filter(University.id == id_f).first()
        country = None
        occupation = None
    else:
        occupation = Occupation.query.filter(Occupation.id == id_f).first()
        university = None
        country = None
    if files:
        object = None
        for file in files:
            if file and checkFile(file.filename):
                img_name = secure_filename(file.filename)
                app.config["UPLOAD_FOLDER"] = img_file2 + file_url
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
                img_url = f'{img_file}{file_url}/{img_name}'
                if file_url == 'country_img':
                    img = Images(img=img_url, country_id=country.id, file_type_id=file_type.id)
                    img.add()
                    object = country.json()
                elif file_url == 'university_img':
                    img = Images(img=img_url, university_id=university.id, file_type_id=file_type.id)
                    img.add()
                    object = university.json()
                else:
                    img = Images(img=img_url, occupation_id=occupation.id, file_type_id=file_type.id)
                    img.add()
                    object = occupation.json()
            else:
                return jsonify({
                    'status': False
                })
        return jsonify({
            'status': True,
            'object': object,
            'text': Messages.register_img()
        })
    else:
        return jsonify({
            'status': False
        })

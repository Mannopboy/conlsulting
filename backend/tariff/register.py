from app import *
from backend.settings.settings import *
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required


@app.route(f'{api}/get_tariff')
@jwt_required()
def get_tariff():
    tariff_all = Tariff.query.order_by(Tariff.id).all()
    data = []
    for tariff in tariff_all:
        data.append(tariff.json())
    return jsonify({
        'status': True,
        'data': data,
    })


@app.route(f'{api}/delete_package/<int:package_id>', methods=['DELETE'])
@jwt_required()
def delete_package(package_id):
    package = Package.query.filter(Package.id == package_id).first()
    package.deleted = True
    db.session.commit()
    return jsonify({
        'status': True
    })


@app.route(f'{api}/change_package', methods=['POST'])
@jwt_required()
def change_package():
    form = json.dumps(dict(request.form))
    data = json.loads(form)
    req = eval(data['res'])
    package_id = req['id']

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


@app.route(f'{api}/get_package', methods=['POST'])
@jwt_required()
def get_package():
    id = request.get_json()
    tariff = Tariff.query.filter(Tariff.id == id).first()
    return jsonify({
        'status': True,
        'tariff': tariff.json(),
    })


@app.route(f'{api}/register_package', methods=['POST'])
@jwt_required()
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


@app.route(f'{api}/register_tariff', methods=['POST'])
@jwt_required()
def register_tariff():
    req = request.get_json()

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


@app.route(f'{api}/register_connect', methods=['POST'])
@jwt_required()
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

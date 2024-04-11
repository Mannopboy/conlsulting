from app import request, app, jsonify, json, db
from backend.settings.settings import check_payment, api, Messages, checkFile, img_file3, package_img, img_file
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from datetime import date
from backend.models.basic_model import Tariff, Package, User, StudentConnectedTariff, AdditionTariff, Cost
import os


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
        'status': True,
        'text': Messages.delete_package()
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
        if file and checkFile(file.filename):
            if package.img:
                os.remove(f'{img_file3}{package.img}')
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = package_img()
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = img_file + 'package_img/' + img_name
            package.img = img_url
            package.status = True
    else:
        link = req['link']
        package.status = False
        package.link = link
    db.session.commit()
    return jsonify({
        'status': True,
        'package': package.json(),
        'text': Messages.change()
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
        if file and checkFile(file.filename):
            img_name = secure_filename(file.filename)
            app.config["UPLOAD_FOLDER"] = package_img()
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))
            img_url = img_file + 'package_img/' + img_name
            package = Package(name=title, text=textarea, tariff_id=tariff.id, img=img_url, status=True, deleted=False)
            package.add()
            return jsonify({
                'status': True,
                'package': package.json(),
                'text': Messages.register_package()
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
            'package': package.json(),
            'text': Messages.register_package()
        })


@app.route(f'{api}/add_connect', methods=['POST'])
@jwt_required()
def add_connect():
    req = request.get_json()
    print(request.get_json())
    user_id = req['user_id']
    tariff_id = req['tariff_id']
    list = req['list']
    today = date.today()
    student = User.query.filter(User.id == user_id).first()
    tariff = Tariff.query.filter(Tariff.id == tariff_id).first()
    connected_student = StudentConnectedTariff.query.filter(StudentConnectedTariff.student_id == student.id,
                                                            StudentConnectedTariff.tariff_id == tariff.id).order_by(
        StudentConnectedTariff.id).all()
    if not connected_student and list:
        for item in list:
            connected_student = StudentConnectedTariff(student_id=student.id, tariff_id=tariff.id, date=today,
                                                       country_id=item['country_id'],
                                                       university_id=item['university_id'],
                                                       occupation_id=item['occupation_id'])
            connected_student.add()
        cost = Cost(cost=int(tariff.cost), student_id=student.id, date=today)
        cost.add()
        return jsonify({
            'status': check_payment(student.id),
            'text': Messages.add_connect()
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/change_tariffs', methods=['PUT'])
@jwt_required()
def change_tariffs():
    req = request.get_json()
    tariff_id = req['id']
    name = req['name']
    cost = req['cost']
    color = req['color']
    number = req['number']
    additions = req['selectedSubs']
    tariff = Tariff.query.filter(Tariff.id == tariff_id).first()
    if tariff:
        tariff.name = name
        tariff.cost = cost
        tariff.number = number
        tariff.color = color
        addition_tariff = AdditionTariff.query.filter(AdditionTariff.first_tariff == tariff.id).order_by(
            AdditionTariff.id).all()
        for old_addition_tariff in addition_tariff:
            AdditionTariff.query.filter(AdditionTariff.first_tariff == old_addition_tariff.first_tariff).delete()
            db.session.commit()
        for addition in additions:
            addition_tariff = AdditionTariff(first_tariff=tariff.id, second_tariff=addition)
            addition_tariff.add()
        return jsonify({
            'status': True,
            'tariff': tariff.json(),
            'text': Messages.change_tariff()
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/register_tariff', methods=['POST'])
@jwt_required()
def register_tariff():
    req = request.get_json()

    name = req['name']
    cost = req['cost']
    color = req['color']
    number = req['number']
    additions = req['selectedSubs']
    tariff = Tariff.query.filter(Tariff.name == name).first()
    if not tariff:
        tariff = Tariff(name=name, color=color, cost=cost, number=number)
        tariff.add()
        for addition in additions:
            addition_tariff = AdditionTariff(first_tariff=tariff.id, second_tariff=addition)
            addition_tariff.add()
        return jsonify({
            'status': True,
            'tariff': tariff.json(),
            'text': Messages.register_tariff()
        })
    else:
        return jsonify({
            'status': False
        })

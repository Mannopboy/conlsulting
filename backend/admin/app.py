from app import request, app, jsonify, db
from backend.settings.settings import check_account_types, admin_code, api, add_account, delete_account, Messages
from flask_jwt_extended import jwt_required
from datetime import date
from backend.models.basic_model import User, AccountType, Payment


# @app.route(f'{api}/test')
# def test():
#
#     return jsonify({
#         'status': True
#     })


@app.route(f'{api}/delete_payment/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete_payment(payment_id):
    payment = Payment.query.filter(Payment.id == payment_id).first()
    payment.deleted = True
    db.session.commit()
    return jsonify({
        'status': delete_account(payment.id),
        'text': Messages.delete_payment()
    })


@app.route(f'{api}/undelete_payment/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def undelete_payment(payment_id):
    payment = Payment.query.filter(Payment.id == payment_id).first()
    payment.deleted = False
    db.session.commit()
    return jsonify({
        'status': delete_account(payment.id),
        'text': Messages.undelete_payment()
    })


@app.route(f'{api}/get_account_types', methods=['GET'])
@jwt_required()
def get_account_types():
    account_types = AccountType.query.order_by(AccountType.id).all()
    list = []
    for account_type in account_types:
        list.append(account_type.json())
    return jsonify({
        'status': True,
        'account_types': list
    })


@app.route(f'{api}/change_payment_account_type', methods=['PUT'])
@jwt_required()
def change_payment_account_type():
    payment_id = request.get_json()['payment_id']
    account_type_id = request.get_json()['account_type_id']
    payment = Payment.query.filter(Payment.id == payment_id).first()
    account_type = AccountType.query.filter(AccountType.id == account_type_id).first()
    if payment and account_type:
        payment.account_type_id = account_type.id
        db.session.commit()
        return jsonify({
            'status': True,
            'payment': payment.json(),
            'text': Messages.change()
        })
    else:
        return jsonify({
            'status': False,
            'text': Messages.dont_change()
        })


@app.route(f'{api}/add_payment/<int:account_type_id>', methods=['POST'])
@jwt_required()
def add_payment(account_type_id):
    student_id = request.get_json()['student_id']
    payment = int(request.get_json()['payment'])
    today = date.today()
    new_payment = Payment(pay=payment, student_id=student_id, account_type_id=account_type_id, date=today)
    new_payment.add()
    status = add_account(new_payment.id)
    print(status)
    return jsonify({
        'status': status,
        'text': Messages.add_payment()
    })


@app.route(f'{api}/get_student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    user = User.query.filter(User.id == student_id).first()
    if user:
        return jsonify({
            'status': True,
            'data': user.personal_json()
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/get_payments/<int:user_id>', methods=['GET'])
@jwt_required()
def get_payments(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user.role == admin_code:
        payments = Payment.query.filter(Payment.deleted == False).order_by(Payment.id).all()
        print(payments)
        list = []
        for payment in payments:
            list.append(payment.json())
        return jsonify({
            'status': True,
            'list': list
        })
    else:
        return jsonify({
            'status': False
        })


@app.route(f'{api}/get_deleted_payments/<int:user_id>', methods=['GET'])
@jwt_required()
def get_deleted_payments(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user.role == admin_code:
        payments = Payment.query.filter(Payment.deleted == True).order_by(Payment.id).all()
        list = []
        for payment in payments:
            list.append(payment.json())
        return jsonify({
            'status': True,
            'list': list
        })
    else:
        return jsonify({
            'status': False
        })

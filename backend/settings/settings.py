from app import app
import universities
import pycountry
from allcities import cities
import os
from werkzeug.security import generate_password_hash
from backend.models.basic_model import User, AccountType, FileType, Country, University, City, Account, Payment, db, \
    Cost
from datetime import datetime


def check_payment(user_id):
    user = User.query.filter(User.id == user_id).first()
    payments = Payment.query.filter(Payment.student_id == user.id).order_by(Payment.id).all()
    costs = Cost.query.filter(Cost.student_id == user.id).order_by(Cost.id).all()
    balance = 0
    for payment in payments:
        balance += payment.pay
    for cost in costs:
        balance -= cost.cost
    if balance >= 0:
        return True
    else:
        return False


def admin():
    admin_base = User.query.filter(User.id == 1).first()
    if not admin_base:
        hashed = generate_password_hash(password='123')
        new_admin = User(username='admin', name='admin', password=hashed, role=admin_code)
        new_admin.add()
        return True


class Messages:
    @staticmethod
    def delete_student():
        return "Student o'chirildi"

    @staticmethod
    def undelete_student():
        return "Student qaytib qo'shildi"

    @staticmethod
    def change_user():
        return "Sizning malumotingiz o'zgartirildi"

    @staticmethod
    def register_addition_file():
        return "Qo'shimcha fayl qo'shildi"

    @staticmethod
    def register_img():
        return "Fayl qo'shildi"

    @staticmethod
    def register():
        return "Registratiya bo'ldi"

    @staticmethod
    def login():
        return "Login bo'ldi"

    @staticmethod
    def logout():
        return "Logout bo'ldi"

    @staticmethod
    def change():
        return "Malumot o'zgardi"

    @staticmethod
    def dont_change():
        return "Malumot o'zgarmadi"

    @staticmethod
    def delete_payment():
        return "To'lov o'chirildi"

    @staticmethod
    def undelete_payment():
        return "To'lov qayta qo'shildi"

    @staticmethod
    def add_payment():
        return "To'lov qo'shildi"

    @staticmethod
    def delete_package():
        return "Package o'chirildi"

    @staticmethod
    def register_package():
        return "Package qo'shildi"

    @staticmethod
    def add_connect():
        return "Obuna bo'ldingiz"

    @staticmethod
    def change_tariff():
        return "Tariff o'zgardi"

    @staticmethod
    def register_tariff():
        return

    @staticmethod
    def register_university():
        return "Universitet qo'shildi"

    @staticmethod
    def change_country():
        return "Davlat o'zgardi"

    @staticmethod
    def change_occupation():
        return "Soha o'zgardi"

    @staticmethod
    def register_occupation():
        return "Soha qo'shildi"

    def __str__(self):
        return "Bu class xabarlarni saqlash uchun"


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return value and type_file


def delete_account(payment_id):
    payment = Payment.query.filter(Payment.id == payment_id).first()
    year = payment.date.strftime('%Y')
    month = payment.date.strftime('%m')
    if payment:
        accounts = Account.query.order_by(Account.id).all()
        for account in accounts:
            if account.date.strftime('%Y') == year and account.date.strftime('%m') == month:
                account_id = account.id
                account = Account.query.filter(Account.id == account_id).first()
                account.balance -= payment.pay
                if payment.account_type_id == 1:
                    if account.cash:
                        account.cash -= payment.pay
                    else:
                        account.cash = payment.pay
                elif payment.account_type_id == 2:
                    if account.click:
                        account.click -= payment.pay
                    else:
                        account.click = payment.pay
                elif payment.account_type_id == 3:
                    if account.bank:
                        account.bank -= payment.pay
                    else:
                        account.bank = payment.pay
                db.session.commit()
                return True
    else:
        return False


def add_account(payment_id):
    payment = Payment.query.filter(Payment.id == payment_id).first()
    year = payment.date.strftime('%Y')
    month = payment.date.strftime('%m')
    if payment:
        accounts = Account.query.order_by(Account.id).all()
        account_id = False
        if accounts:
            for account in accounts:
                if account.date.strftime('%Y') == year and account.date.strftime('%m') == month:
                    account_id = account.id
        if account_id:
            account = Account.query.filter(Account.id == account_id).first()
            try:
                account.balance += payment.pay
                if payment.account_type_id == 1:
                    account.cash += payment.pay
                elif payment.account_type_id == 2:
                    account.click += payment.pay
                elif payment.account_type_id == 3:
                    account.bank += payment.pay
                db.session.commit()
            except TypeError:
                account.balance = payment.pay
                if payment.account_type_id == 1:
                    account.cash = payment.pay
                elif payment.account_type_id == 2:
                    account.click = payment.pay
                elif payment.account_type_id == 3:
                    account.bank = payment.pay
                db.session.commit()
            return True
        else:
            date = payment.date.strftime('%Y-%m')
            date = datetime.strptime(date, "%Y-%m")
            new_account = Account(date=date, balance=payment.pay)
            new_account.add()
            if payment.account_type_id == 1:
                new_account.cash = payment.pay
            elif payment.account_type_id == 2:
                new_account.click = payment.pay
            elif payment.account_type_id == 3:
                new_account.bank = payment.pay
            db.session.commit()
            return True
    else:
        return False


api = '/api'
admin_code = '9sv8s90vd8'
student_code = '09df5vd0fv'

img_file = 'static/img/'
img_file2 = 'frontend/build/static/img/'
img_file3 = 'frontend/build/'
list_file = [
    {
        'name': 'school_profile',
        'status': True
    }, {
        'name': 'school_report',
        'status': True
    }, {
        'name': 'high_school_transcript',
        'status': True
    }, {
        'name': 'IELTS_certificate',
        'status': True
    }, {
        'name': 'sat_certificate',
        'status': True
    }, {
        'name': 'other_certificates',
        'status': True
    }, {
        'name': 'income_statement_of_parents',
        'status': True
    }, {
        'name': 'personal_statement',
        'status': True
    }, {
        'name': 'recommendation_letters',
        'status': True
    }, {
        'name': 'additional',
        'status': True
    }, {
        'name': 'resume',
        'status': True
    }, {
        'name': 'user_img',
        'status': False
    }, {
        'name': 'package_img',
        'status': False
    }, {
        'name': 'passport_upload',
        'status': False
    }, {
        'name': 'addition_file',
        'status': False
    }, {
        'name': 'university_img',
        'status': False
    }, {
        'name': 'country_img',
        'status': False
    }, {
        'name': 'occupation_img',
        'status': False
    },
]
account_types = [
    'Cash',
    'Click',
    'Bank'
]


# def current_user():
#     get_user = None
#     if 'username' in session:
#         get_user = User.query.filter(User.username == session['username']).first()
#         # get_user = User.query.filter(User.id == 10).first()
#     return get_user


def check_account_types():
    for account_type in account_types:
        old_account_types = AccountType.query.filter(AccountType.name == account_type).first()
        if not old_account_types:
            new_account_types = AccountType(name=account_type)
            new_account_types.add()


def check_file_type():
    app.config["UPLOAD_FOLDER"] = img_file2
    for type in list_file:
        name = img_file2 + type['name']
        app.config["UPLOAD_FOLDER"] = name
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"]), exist_ok=True)
        type_file_old = FileType.query.filter(FileType.name == type['name']).first()
        if not type_file_old:
            type_file_new = FileType(name=type['name'], status=type['status'])
            type_file_new.add()


def package_img():
    upload_folder = f"{img_file2}package_img/"
    return upload_folder


def add_countries():
    with app.app_context():
        countries = pycountry.countries
        for state in countries:
            country_old = Country.query.filter(Country.name == state.name).first()
            if not country_old:
                # CountryClass(state.name).add_university()
                country_new = Country(name=state.name, code=state.alpha_2)
                country_new.add()
            else:
                # CountryClass(state.name).add_university()
                country_old.code = state.alpha_2
                db.session.commit()
        return True


class CountryClass:
    def __init__(self, name):
        self.name = name

    def get_universities(self):
        country = Country.query.filter(Country.name == self.name).first()
        university_list = []
        for university in country.universities:
            info = {
                'name': university.name,
                'web_pages': university.web_pages,
            }
            university_list.append(info)
        return university_list

    def add_university(self):
        with app.app_context():
            uni = universities.API()
            canadian = uni.search(country=self.name)
            country = Country.query.filter(Country.name == self.name).first()
            for university in canadian:
                university_old = University.query.filter(University.name == university.name).first()
                if not university_old:
                    university_new = University(name=university.name, web_pages=university.web_pages[0],
                                                country_id=country.id)
                    university_new.add()
                else:
                    university_old.web_pages = university.web_pages[0]
                    db.session.commit()
            return True

    def add_city(self):
        country = Country.query.filter(Country.name == self.name).first()
        gg = cities.filter(country_code=country.code)
        for city in gg:
            city_old = City.query.filter(City.name == city.name, City.county_id == country.id).first()
            if not city_old:
                city_new = City(name=city.name, county_id=country.id)
                city_new.add()
        return True

    def get_country(self):
        with app.app_context():
            state = Country.query.filter(Country.name == self.name).first()
            object = {
                'country': state.json(),
                'cities': []
            }
            for city in state.cities:
                object['cities'].append(city.json())
            return object

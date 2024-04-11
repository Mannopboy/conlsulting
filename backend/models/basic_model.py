from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import *
from datetime import datetime
import uuid

url = 'http://192.168.1.107:5000/'

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('backend.models.config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db


class Student(db.Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    uu_id = Column(String, default=uuid.uuid4())
    parent_name = Column(String, default='')
    parent_surname = Column(String, default='')
    country_of_address_id = Column(Integer, ForeignKey('country.id'))
    country_of_work_id = Column(Integer, ForeignKey('country.id'))
    country_of_address = db.relationship("Country", foreign_keys=[country_of_address_id])
    country_of_work = db.relationship("Country", foreign_keys=[country_of_work_id])
    date_birth = Column(Date)
    position = Column(String, default='')
    parent_phone_number = Column(String, default='')
    parent_passport_number = Column(String, default='')
    parent_passport_expiration = Column(String, default='')
    student_connected_tariff = db.relationship('StudentConnectedTariff', backref='student',
                                               order_by='StudentConnectedTariff.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        date_birth = None
        if self.date_birth:
            date_birth = self.date_birth.strftime('%Y-%m-%d')
        info = [
            {
                "value": self.parent_name,
                'name': 'parent_name',
                "order": 0
            }, {
                "value": self.parent_surname,
                'name': 'parent_surname',
                "order": 1
            }, {
                "value": self.country_of_address_id,
                'name': 'address',
                "order": 2
            }, {
                "value": date_birth,
                'name': 'date_birth',
                "order": 3
            }, {
                "value": self.country_of_work_id,
                'name': 'place_of_work',
                "order": 4
            }, {
                "value": self.position,
                'name': 'position',
                "order": 5
            }, {
                "value": self.parent_phone_number,
                'name': 'parent_phone_number',
                "order": 6
            }, {
                "value": self.parent_passport_number,
                'name': 'parent_passport_number',
                "order": 7
            }, {
                "value": self.parent_passport_expiration,
                'name': 'parent_passport_expiration',
                "order": 8
            },
        ]
        return info


class FileType(db.Model):
    __tablename__ = 'file_type'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    status = Column(Boolean)
    files = db.relationship('File', backref='type',
                            order_by='File.id')
    images = db.relationship('Images', backref='type',
                             order_by='Images.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'name': {
                "value": self.name,
                "order": 0
            }
        }
        return info


class AdditionFile(db.Model):
    __tablename__ = 'addition_file'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    file = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    file_name = Column(String)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        if self.file:
            status = True
        else:
            status = False
        info = {
            'img_type': self.file_name,
            'status': status
        }
        return info


class File(db.Model):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    file = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    file_type_id = Column(Integer, ForeignKey('file_type.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'img': {
                "value": f'{url}/{self.file}',
                "order": 0
            }, 'img_type': {
                "value": self.type,
                "order": 2
            }
        }
        return info


class Images(db.Model):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    img = Column(String)
    country_id = Column(Integer, ForeignKey('country.id'))
    university_id = Column(Integer, ForeignKey('university.id'))
    occupation_id = Column(Integer, ForeignKey('occupation.id'))
    file_type_id = Column(Integer, ForeignKey('file_type.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'id': self.id,
            'img': f'{url}/{self.img}',
        }
        return info


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    username = Column(String)
    passport_number = Column(String, default='')
    name = Column(String, default='')
    surname = Column(String, default='')
    country_id = Column(Integer, ForeignKey('country.id'))
    school_studied = Column(String, default='')
    address = Column(String, default='')
    nationality = Column(String, default='')
    email = Column(String, default='')
    password = Column(String, default='')
    role = Column(String, default='')
    number = Column(String, default='')
    date_birth = Column(Date)
    deleted = Column(Boolean, default=False)
    student = db.relationship('Student', uselist=False, backref='user',
                              order_by='Student.id')
    files = db.relationship('File', backref='user',
                            order_by='File.id')
    addition_files = db.relationship('AdditionFile', backref='user',
                                     order_by='AdditionFile.id')

    payments = db.relationship('Payment', backref='student',
                               order_by='Payment.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def personal_json(self):
        passport_upload = None
        for img in self.files:
            if img.file_type_id == 14:
                passport_upload = True
        info = [
            {
                "value": self.name,
                'name': 'name',
                "order": 0
            }, {
                "value": self.surname,
                'name': 'surname',
                "order": 1
            }, {
                "value": self.passport_number,
                'name': 'passport_number',
                "order": 7
            }, {
                "value": self.address,
                'name': 'address',
                "order": 3
            }, {
                "value": self.date_birth,
                'name': 'date_birth',
                "order": 4
            }, {
                "value": self.country_id,
                'name': 'place_of_birth',
                "order": 5
            }, {
                "value": self.school_studied,
                'name': 'school_studied',
                "order": 6
            }, {
                "value": passport_upload,
                'name': 'passport_upload',
                "order": 8
            }
        ]

        return info

    def list_json(self):
        balance = 0
        payments = Payment.query.filter(Payment.student_id == self.id).order_by(Payment.id).all()
        costs = Cost.query.filter(Cost.student_id == self.id).order_by(Cost.id).all()
        for payment in payments:
            balance += payment.pay
        for cost in costs:
            balance -= cost.cost
        user_img = None
        for img in self.files:
            if img.file_type_id == 12:
                user_img = f'{url}/{img.file}',
        date = datetime.today()
        if self.date_birth:
            age = date.year - int(self.date_birth.strftime('%Y'))
        else:
            age = None
        info = {
            'id': self.id,
            'user_img': user_img,
            'full_name': f'{self.name} {self.surname}',
            'number': self.number,
            'age': age,
            'balance': balance,
        }
        return info

    def json(self):
        date_birth = None
        if date_birth:
            date_birth = self.date_birth
        user_img = None
        for img in self.files:
            if img.file_type_id == 12:
                user_img = f'{url}{img.file}',
        passport_upload = None
        for img in self.files:
            if img.file_type_id == 14:
                passport_upload = True
            else:
                passport_upload = False
        info = {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "user_id": self.id,
            "user_img": user_img,
            'extra_data': [
                {
                    "value": self.passport_number,
                    'name': 'passport_number',
                    "order": 6
                }, {
                    "value": self.address,
                    'name': 'address',
                    "order": 2
                }, {
                    "value": self.nationality,
                    'name': 'nationality',
                    "order": 5
                }, {
                    "value": self.email,
                    'name': 'email',
                    "order": 0
                }, {
                    "value": self.number,
                    'name': 'number',
                    "order": 1
                }, {
                    "value": date_birth,
                    'name': 'date_birth',
                    "order": 3
                }, {
                    "value": self.country_id,
                    'name': 'country_id',
                    "order": 4
                }, {
                    "value": passport_upload,
                    'name': 'passport_upload',
                    "order": 7
                }
            ]
        }
        return info


class AccountType(db.Model):
    __tablename__ = "account_type"
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    payments = db.relationship('Payment', backref='account_type',
                               order_by='Payment.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'id': self.id,
            'name': self.name,
        }
        return info


class Payment(db.Model):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    pay = Column(BigInteger)
    date = Column(Date)
    deleted = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey('user.id'))
    account_type_id = Column(Integer, ForeignKey('account_type.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'id': self.id,
            'full_name': f'{self.student.surname} {self.student.name}',
            'pay': self.pay,
            'account_type': self.account_type.name,
            'date': self.date.strftime('%Y-%m-%d'),
        }
        return info


class Cost(db.Model):
    __tablename__ = "cost"
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    cost = Column(BigInteger)
    date = Column(Date)
    deleted = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey('user.id'))
    account_type_id = Column(Integer, ForeignKey('account_type.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'id': self.id,
            'full_name': f'{self.student.surname} {self.student.name}',
            'pay': self.pay,
            'account_type': self.account_type.name,
            'date': self.date.strftime('%Y-%m-%d'),
        }
        return info


class Occupation(db.Model):
    __tablename__ = 'occupation'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    university_occupation = db.relationship('UniversityOccupation', backref='occupation',
                                            order_by='UniversityOccupation.id')
    images = db.relationship('Images', backref='occupation',
                             order_by='Images.id')
    student_connected_tariff = db.relationship('StudentConnectedTariff', backref='occupation',
                                               order_by='StudentConnectedTariff.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        list = []
        for file in self.images:
            list.append(file.json())
        info = {
            'id': self.id,
            'name': self.name,
            'images': list
        }
        return info


class UniversityOccupation(db.Model):
    __tablename__ = 'university_occupation'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    university_id = Column(Integer, ForeignKey('university.id'))
    occupation_id = Column(Integer, ForeignKey('occupation.id'))
    price = Column(Integer)

    def add(self):
        db.session.add(self)
        db.session.commit()


class University(db.Model):
    __tablename__ = 'university'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    place = Column(String)
    web_pages = Column(String)
    price = Column(Integer)
    stipend = Column(Integer)
    country_id = Column(Integer, ForeignKey('country.id'))
    university_occupation = db.relationship('UniversityOccupation', backref='university',
                                            order_by='UniversityOccupation.id')
    images = db.relationship('Images', backref='university',
                             order_by='Images.id')
    student_connected_tariff = db.relationship('StudentConnectedTariff', backref='university',
                                               order_by='StudentConnectedTariff.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        list = []
        list2 = []
        for file in self.images:
            list.append(file.json())
        for occupation in self.university_occupation:
            list2.append(occupation.occupation.json())
        info = {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'web_pages': self.web_pages,
            'price': self.price,
            'country': self.country.json(),
            'occupations': list2,
            'images': list
        }
        return info


class Country(db.Model):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    official_name = Column(String)
    code = Column(String)
    universities = db.relationship('University', backref='country', order_by='University.id')
    cities = db.relationship('City', backref='country', order_by='City.id')
    users = db.relationship('User', backref='country', order_by='User.id')
    images = db.relationship('Images', backref='country',
                             order_by='Images.id')
    student_connected_tariff = db.relationship('StudentConnectedTariff', backref='country',
                                               order_by='StudentConnectedTariff.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        list = []
        for file in self.images:
            list.append(file.json())
        info = {
            'id': self.id,
            'name': self.name,
            'images': list
            # 'official_name': self.official_name
        }
        return info


class City(db.Model):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    county_id = Column(Integer, ForeignKey('country.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'name': self.name,
            'county': self.county.name
        }
        return info


class AdditionTariff(db.Model):
    __tablename__ = 'addition_tariff'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    first_tariff = Column(Integer, ForeignKey('tariff.id'))
    second_tariff = Column(Integer, ForeignKey('tariff.id'))
    first = db.relationship("Tariff", foreign_keys=[first_tariff])
    second = db.relationship("Tariff", foreign_keys=[second_tariff])

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'name': self.first,
            'packages': self.second
        }
        return info


class Tariff(db.Model):
    __tablename__ = 'tariff'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    color = Column(String)
    number = Column(Integer, default=1)
    deleted = Column(Boolean, default=False)
    cost = Column(String)
    packages = db.relationship('Package', backref='tariff', order_by='Package.id')
    student_connected_tariff = db.relationship('StudentConnectedTariff', backref='tariff',
                                               order_by='StudentConnectedTariff.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        package_all = []
        addition_tariffs = []
        additionTariff = AdditionTariff.query.filter(AdditionTariff.first_tariff == self.id).order_by(
            AdditionTariff.id).all()
        for package in self.packages:
            if not package.deleted:
                package_all.append(package.json())
        for tariff in additionTariff:
            tariff = Tariff.query.filter(Tariff.id == tariff.second_tariff).first()

            if tariff and tariff.packages:
                for package in tariff.packages:
                    if not package.deleted:
                        package_all.append(package.json())
        for tariff in additionTariff:
            if tariff.first_tariff == self.id:
                info = {
                    'id': tariff.second.id,
                    'name': tariff.second.name
                }
                addition_tariffs.append(info)
        info = {
            'id': self.id,
            'name': self.name,
            'cost': self.cost,
            'number': self.number,
            'color': self.color,
            'packages': package_all,
            'addition_tariffs': addition_tariffs
        }
        return info


class Package(db.Model):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    name = Column(String)
    text = Column(String)
    link = Column(String)
    status = Column(Boolean)
    img = Column(String)
    deleted = Column(Boolean, default=False)
    tariff_id = Column(Integer, ForeignKey('tariff.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'id': self.id,
            'name': self.name,
            'tariff_id': self.tariff_id,
            'text': self.text,
            'link': self.link,
            'status': self.status,
            'img': f'{url}/{self.img}',
        }
        return info


class StudentConnectedTariff(db.Model):
    __tablename__ = 'student_connected_tariff'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    date = Column(Date)
    deleted = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey('student.id'))
    tariff_id = Column(Integer, ForeignKey('tariff.id'))
    country_id = Column(Integer, ForeignKey('country.id'))
    university_id = Column(Integer, ForeignKey('university.id'))
    occupation_id = Column(Integer, ForeignKey('occupation.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'id': self.id,
            'name': self.name,
            'tariff_id': self.tariff_id,
        }
        return info


class Account(db.Model):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    uu_id = Column(String, default=uuid.uuid4())
    balance = Column(BigInteger, default=0)
    date = Column(Date)
    bank = Column(BigInteger, default=0)
    cash = Column(BigInteger, default=0)
    click = Column(BigInteger, default=0)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        info = {
            'balance': self.balance,
            'bank': self.bank,
            'cash': self.cash,
            'click': self.click
        }
        return info

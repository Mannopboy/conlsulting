from app import *
import universities
import pycountry
from allcities import cities
import os

api = '/api'

img_file = 'media/img/'
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
    },
]


def current_user():
    get_user = None
    if 'username' in session:
        get_user = User.query.filter(User.username == session['username']).first()
        # get_user = User.query.filter(User.id == 10).first()
    return get_user


def check_file_type():
    app.config["UPLOAD_FOLDER"] = img_file
    for type in list_file:
        name = img_file + type['name']
        app.config["UPLOAD_FOLDER"] = name
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"]), exist_ok=True)
        type_file_old = FileType.query.filter(FileType.name == type['name']).first()
        if not type_file_old:
            type_file_new = FileType(name=type['name'], status=type['status'])
            type_file_new.add()


def user_img():
    upload_folder = f"{img_file}user_img/"
    return upload_folder


def package_img():
    upload_folder = f"{img_file}package_img/"
    return upload_folder


def add_countries():
    with app.app_context():
        countries = pycountry.countries
        for state in countries:
            country_old = Country.query.filter(Country.name == state.name).first()
            if not country_old:
                country_new = Country(name=state.name, official_name=state.official_name, code=state.alpha_2)
                country_new.add()
            else:
                country_old.official_name = state.official_name
                country_old.code = state.alpha_2
                db.session.commit()
        return True


class CountryClass:
    def __init__(self, name):
        self.name = name

    def get_universities(self):
        country = Country.query.filter(Country.name == self.name).first()
        university_list = []
        print(len(country.universities))
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

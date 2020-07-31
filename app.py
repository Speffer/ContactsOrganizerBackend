import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_json import FlaskJSON

from db import db
from resources.company import Company, CompanyById, CompanyType
from resources.contact import Contact, ContactById

from models.company import CompanyModel, CompanyPFModel, CompanyPJModel
from models.contact import ContactModel, PhoneModel

app = Flask(__name__)
api = Api(app)
json = FlaskJSON(app)

basedir = os.path.abspath(os.path.dirname(__file__))
DB_URL = 'sqlite:///' + os.path.join(basedir, 'data.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Migrations Config
migrate = Migrate(app, db)
CompanyModel
CompanyPJModel
CompanyPFModel
ContactModel
PhoneModel

# Routes
api.add_resource(Contact, '/contact')
api.add_resource(ContactById, '/contact/<int:id>')
api.add_resource(Company, '/company')
api.add_resource(CompanyById, '/company/<int:id>')
api.add_resource(CompanyType, '/company/type/<int:id>')

db.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

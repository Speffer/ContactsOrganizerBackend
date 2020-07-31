from db import db
import json
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class ContactModel(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship('CompanyModel')
    phones = db.relationship('PhoneModel', backref='contacts', lazy=True)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, name, company, company_id, phones):
        self.name = name
        self.company = company
        self.company_id = company_id
        self.phones = phones

    def json(self):
        return {
            'name': self.name,
            'company': self.company,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
            'phones': self.phones
        }
    
    @property
    def all_json(self):
        return {
            'name': self.name,
            'company': self.company,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
            'phones': self.phones
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PhoneModel(db.Model):
    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    contact = db.relationship('ContactModel')
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, number, contact_id, contact):
        self.number = number
        self.contact_id = contact_id
        self.contact = contact

    def json(self):
        return {
            'number': self.number,
            'contact_id': self.contact_id,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
            'contact': self.contact
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

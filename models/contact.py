from db import db
import json
from flask import jsonify
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

    def __init__(self, name, company_id):
        self.name = name
        self.company_id = company_id

    def json(self):
        phones = []
        for p in self.phones:
            phones.append(p.json())

        return {
            'name': self.name,
            'company': self.company.json(),
            'company_id': self.company_id,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
            'phones': phones
        }
    
    @property
    def all_json(self):
        phones = []
        for p in self.phones:
            phones.append(p.json())

        return {
            'name': self.name,
            'company': self.company.json(),
            'company_id': self.company_id,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
            'phones': phones
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_company_id(cls, id):
        return cls.query.filter_by(company_id=id).all()

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

    def __init__(self, number, contact_id):
        self.number = number
        self.contact_id = contact_id

    def json(self):
        return {
            'number': self.number,
            'contact_id': self.contact_id,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
        }

    @property
    def all_json(self):
        return {
            'number': self.number,
            'contact_id': self.contact_id,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_contact_id(cls, id):
        return cls.query.filter_by(contact_id=id).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

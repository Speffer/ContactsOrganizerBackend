from db import db
import json
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class CompanyModel(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    document = db.Column(db.String(80))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, name, city, document):
        self.name = name
        self.city = city
        self.document = document

    @property
    def all_json(self):
        return {
            'name': self.name,
            'city': self.city,
            'document': self.document,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str)
        }

    def json(self):
        return {
            'name': self.name,
            'city': self.city,
            'document': self.document,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str)
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


class CompanyPJModel(db.Model):
    __tablename__ = 'companies_pj'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship('CompanyModel')
    fantasy_name = db.Column(db.String(80))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, company_id, fantasy_name):
        self.company_id = company_id
        self.fantasy_name = fantasy_name

    def json(self):
        return {
            'fantasy_name': self.fantasy_name,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
            'company_id': self.company_id,
            'company': self.company.json()
        }

    @property
    def all_json(self):
        return {
            'fantasy_name': self.fantasy_name,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str),
            'company': self.company,
            'company_id': self.company_id,
            'company': self.company.json()
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_company_id(cls, company_id):
        return cls.query.filter_by(company_id=company_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class CompanyPFModel(db.Model):
    __tablename__ = 'companies_pf'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship('CompanyModel')
    rg = db.Column(db.String(80))
    birthday = db.Column(DateTime(timezone=True))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, company_id, rg, birthday):
        self.company_id = company_id
        self.rg = rg
        self.birthday = birthday

    def json(self):
        return {
            'company': self.company.json(),
            'company_id': self.company_id,
            'birthday': json.dumps(self.birthday, default=str),
            'rg': self.rg,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str)
        }

    @property
    def all_json(self):
        return {
            'company': self.company.json(),
            'company_id': self.company_id,
            'birthday': json.dumps(self.birthday, default=str),
            'rg': self.rg,
            'id': self.id,
            'created_at': json.dumps(self.created_at, default=str),
            'updated_at': json.dumps(self.created_at, default=str) if self.updated_at is None else json.dumps(self.updated_at, default=str)
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_company_id(cls, company_id):
        return cls.query.filter_by(company_id=company_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

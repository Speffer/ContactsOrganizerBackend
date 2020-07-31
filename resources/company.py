from flask_restful import Resource, reqparse, inputs
from models.company import CompanyModel, CompanyPFModel, CompanyPJModel
from flask_json import json_response, as_json
from flask import jsonify
import json

class CompanyType(Resource):
    def get(self, id):
        company = CompanyModel.get_by_id(id)
        
        if company:
            if len(company.document) == 13:
                company_pj = CompanyPJModel.get_by_company_id(company.id)
                return company_pj.json(), 200

            elif len(company.document) == 11:
                company_pf = CompanyPFModel.get_by_company_id(company.id)
                return company_pf.json(), 200
            
            else: return {'message': 'Company not found'}, 404
        return {'message': 'Company not found'}, 404

class CompanyById(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        required=True,
        help="Empty name field"
    )
    parser.add_argument(
        'city',
        required=True,
        help="Empty city field"
    )
    parser.add_argument(
        'fantasy_name',
        nullable=True,
    )
    parser.add_argument(
        'rg',
        nullable=True,
    )
    parser.add_argument(
        'birthday',
        nullable=True,
        type=inputs.datetime
    )

    def get(self, id):
        company = CompanyModel.get_by_id(id)
        if company:
            return company.json(), 200
        return {'message': 'Company not found'}, 404
    
    def put(self, id):
        data = Company.parser.parse_args()

        company = CompanyModel.get_by_id(id)
        company.city = data['city']
        company.name = data['name']
        
        if len(company.document) == 13:
            company_pj = CompanyPJModel.get_by_company_id(company.id)
            company_pj.fantasy_name = data["fantasy_name"]

        elif len(company.document) == 11:
            company_pf = CompanyPFModel.get_by_company_id(company.id)
            company_pf.rg = data["rg"]
            company_pf.birthday = data["birthday"]
        
        else:
            return {"message": "Document value is invalid."}, 400
        
        try:
            company.save()
            if len(company.document) == 13: company_pj.save()
            elif len(company.document) == 11: company_pf.save()
        
        except:
            return {"message": "An error occurred inserting the company."}, 500

        return company.json(), 201
    
    def delete(self, id):
        company = CompanyModel.get_by_id(id)
        if company:
            if len(company.document) == 13:
                company_pj = CompanyPJModel.get_by_company_id(id)
                if company_pj:
                    company_pj.delete()

            if len(company.document) == 11:
                company_pf = CompanyPFModel.get_by_company_id(id)
                if company_pf:
                    company_pf.delete() 

            company.delete()
            return {'message': 'Company deleted.'}, 200

        return {'message': 'Company not found.'}, 404


class Company(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'document',
        required=True,
        help="Empty document field"
    )
    parser.add_argument(
        'name',
        required=True,
        help="Empty name field"
    )
    parser.add_argument(
        'city',
        required=True,
        help="Empty city field"
    )
    parser.add_argument(
        'fantasy_name',
        nullable=True,
    )
    parser.add_argument(
        'rg',
        nullable=True,
    )
    parser.add_argument(
        'birthday',
        nullable=True,
        type=inputs.datetime
    )

    def get(self):
        companies = CompanyModel.get_all()
        if companies is not None:
            json_data = jsonify(companies=[c.all_json for c in companies])
            return json_data
        return {'message': 'Company not found'}, 404

    def post(self):
        data = Company.parser.parse_args()
        company_obj = {
            'name': data['name'],
            'city': data['city'],
            'document': data['document']
        }

        company = CompanyModel(**company_obj)
        
        try:
            company.save()

            if len(company.document) == 13:
                pj_obg = {
                    "fantasy_name": data["fantasy_name"],
                    "company_id": company.id
                }
                company_pj = CompanyPJModel(**pj_obg)

                try:
                    company_pj.save()
                except: 
                    return {"message": "An error occurred inserting the company pj."}, 500

            elif len(company.document) == 11:
                pf_obg = {
                    "rg": data["rg"],
                    "birthday": data["birthday"],
                    "company_id": company.id
                }
                company_pf = CompanyPFModel(**pf_obg)

                try:
                    company_pf.save()
                except: 
                    return {"message": "An error occurred inserting the company pf."}, 500
            
            else:
                return {"message": "Document value is invalid."}, 400

        except:
            return {"message": "An error occurred inserting the company."}, 500

        return company.json(), 201
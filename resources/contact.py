from flask_restful import Resource, reqparse
from flask import jsonify
import json
from models.company import CompanyModel, CompanyPFModel, CompanyPJModel
from models.contact import ContactModel, PhoneModel

class ContactById(Resource):
    def get(self, id):
        contact = ContactModel.get_by_id(id)
        if contact:
            return contact.json(), 200
        return {'message': 'Contact not found'}, 404
    
    def delete(self, id):
        contact = ContactModel.get_by_id(id)
        if contact:
            for phone_obj in contact['phones']:
                phone = PhoneModel.get_by_id(phone_obj.id)
                phone.delete()

            contact.delete()
            return {'message': 'Contact deleted.'}, 200

        return {'message': 'Contact not found.'}, 404


class Contact(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        required=True,
        help="Empty name field"
    )
    parser.add_argument(
        'company_id',
        required=True,
        help="Empty company_id field",
        type=int
    )
    parser.add_argument(
        'phones',
        required=True,
        help="Empty phones field",
        type=list
    )

    def get(self):
        contacts = ContactModel.get_all()
        if contacts is not None:
            json_data = jsonify(contacts=[c.all_json for c in contacts])
            return json_data
        return {'message': 'Contact not found'}, 404

    def post(self):
        data = Contact.parser.parse_args()

        contact_obj = {
            'company_id': data['company_id'],
            'name': data['name']
        }
        contact = ContactModel(**contact_obj)
        
        try:
            contact.save()

            for phone_obj in data['phones']:
                phone = PhoneModel(**phone_obj)
                phone.contact_id = contact.id

                try: 
                    phone.save()
                except:
                    return {"message": "An error occurred inserting the phone."}, 500
        except:
            return {"message": "An error occurred inserting the contact."}, 500

        return contact.json(), 201

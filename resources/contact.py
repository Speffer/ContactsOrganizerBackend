from flask_restful import Resource, reqparse
from flask import jsonify, request
import json
from models.company import CompanyModel, CompanyPFModel, CompanyPJModel
from models.contact import ContactModel, PhoneModel

class ContactById(Resource):
    def put(self, id):
        data = request.get_json()
        contact = ContactModel.get_by_id(id)

        if contact: 
            if 'company_id' in data:
                contact.company_id = data['company_id']

            if 'name' in data:
                contact.name = data['name']

            if 'phones' in data and len(data['phones']) > 0:
                phones = PhoneModel.get_by_contact_id(contact.id)

                for index, number in enumerate(data['phones']):
                    if number != phones[index].number and contact.id == phones[index].contact_id:
                        phone_obj = {
                            'number': number,
                            'contact_id': contact.id
                        }
                        new_phone = PhoneModel(**phone_obj)
                        
                        try: 
                            new_phone.save()

                        except:
                            return {"message": "An error occurred inserting the phone."}, 500

            try:
                contact.save()

            except:
                return {"message": "An error occurred inserting the contact."}, 500

            return contact.json(), 201

        else:
            return {"message": "This contact not exist."}, 400

    def get(self, id):
        contact = ContactModel.get_by_id(id)
        if contact:
            return contact.json(), 200
        return {'message': 'Contact not found'}, 404
    
    def delete(self, id):
        contact = ContactModel.get_by_id(id)
        if contact:
            for phone_obj in contact.phones:
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
        action='append'
    )

    def get(self):
        contacts = ContactModel.get_all()
        if contacts is not None:
            json_data = jsonify(contacts=[c.all_json for c in contacts])
            return json_data
        return {'message': 'Contact not found'}, 404

    def post(self):
        data = Contact.parser.parse_args()
        company = CompanyModel.get_by_id(data['company_id'])

        if company: 
            contact_obj = {
                'company_id': data['company_id'],
                'name': data['name']
            }
            contact = ContactModel(**contact_obj)
            
            try:
                contact.save()

                for number in data['phones']:
                    phone_obj = {
                        'number': number,
                        'contact_id': contact.id
                    }
                    phone = PhoneModel(**phone_obj)

                    try: 
                        phone.save()
                    except:
                        return {"message": "An error occurred inserting the phone."}, 500
            except:
                return {"message": "An error occurred inserting the contact."}, 500

            return contact.json(), 201

        else:
            return {"message": "This company not exist."}, 400

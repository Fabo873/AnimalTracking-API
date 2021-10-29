from flask_restful import Resource, reqparse

from models.person import PersonModel
from models.user import UserModel
from helpers.format import returnFormat


class Person(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')
    put_parser.add_argument('first_lastname', type=str, required=True,
                            help='first_lastname is an required param', location='json')
    put_parser.add_argument('second_lastname', type=str, required=True,
                            help='second_lastname is an required param', location='json')
    put_parser.add_argument('user_id', type=str, required=True,
                            help='user_id is an required param', location='json')

    def get(self, id):

        person = PersonModel.find_by_id(id)
        if not person:
            return returnFormat(message='Person not found', status=404)

        return returnFormat(message='Person retrieved succesfully', data=person.json())

    def delete(self, id):

        person = PersonModel.find_by_id(id)
        if not person:
            return returnFormat(message='Person not found', status=404)

        person.delete_from_db()

        return returnFormat(message='Person deleted succesfully')

    def put(self, id):

        data = Person.put_parser.parse_args()

        person = PersonModel.find_by_id(id)
        if not person:
            return returnFormat(message='Person not found', status=404)

        user = UserModel.find_by_id(data['user_id'])
        if not user:
            return returnFormat(message='User not found', status=404)

        if PersonModel.find_by_name(data['name'], data['first_lastname'], data['second_lastname']):
            if person.name != data['name'] or person.first_lastname != data['first_lastname'] or person.second_lastname != data['second_lastname']:
                return returnFormat(message='Person already exists', status=400)

        if user.person.first():
            print(user.person.first().id)
            print(person.id)
            if user.person.first().id != person.id:
                return returnFormat(message='User already has a Person asigned', status=404)

        person.name = data['name']
        person.first_lastname = data['first_lastname']
        person.second_lastname = data['second_lastname']
        person.user_id = data['user_id']

        person.save_to_db()

        return returnFormat(message='Person updated succesfully', data=person.json())


class PersonList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')
    post_parser.add_argument('first_lastname', type=str, required=True,
                             help='first_lastname is an required param', location='json')
    post_parser.add_argument('second_lastname', type=str, required=True,
                             help='second_lastname is an required param', location='json')
    post_parser.add_argument('user_id', type=int, required=True,
                             help='user_id is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of persons to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of persons to retrive', location='args')
    get_parser.add_argument('name', type=str, required=False,
                            help='Name is an required param', location='args')

    def post(self):

        data = PersonList.post_parser.parse_args()

        if PersonModel.find_by_name(data['name'], data['first_lastname'], data['second_lastname']):
            return returnFormat(message='Person already exists', status=400)

        user = UserModel.find_by_id(data['user_id'])
        if not user:
            return returnFormat(message='User not found', status=404)

        if user.person.first():
            return returnFormat(message='User already has a Person asigned', status=404)

        person = PersonModel(**data)

        person.save_to_db()

        return returnFormat(message='Person created succesfully', data=person.json(), status=201)

    def get(self):

        data = PersonList.get_parser.parse_args()
        persons = PersonModel.find_by_attributes(**data)

        return returnFormat(message='Person list retrieved succesfully', data=[person.json() for person in persons])

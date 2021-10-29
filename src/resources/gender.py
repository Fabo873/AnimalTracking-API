from flask_restful import Resource, reqparse

from models.gender import GenderModel
from helpers.format import returnFormat


class Gender(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')

    def get(self, id):

        gender = GenderModel.find_by_id(id)
        if not gender:
            return returnFormat(message='Gender not found', status=404)

        return returnFormat(message='Gender retrieved succesfully', data=gender.json())

    def delete(self, id):

        gender = GenderModel.find_by_id(id)
        if not gender:
            return returnFormat(message='Gender not found', status=404)

        gender.delete_from_db()

        return returnFormat(message='Gender deleted succesfully')

    def put(self, id):

        data = Gender.put_parser.parse_args()

        gender = GenderModel.find_by_id(id)
        if not gender:
            return returnFormat(message='Gender not found', status=404)

        if GenderModel.find_by_name(data['name']) and gender.name != data['name']:
            return returnFormat(message='Gender already exists', status=400)

        gender.name = data['name']

        gender.save_to_db()

        return returnFormat(message='Gender updated succesfully', data=gender.json())


class GenderList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of gender to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of gender to retrive', location='args')

    def post(self):

        data = GenderList.post_parser.parse_args()

        if GenderModel.find_by_name(data['name']):
            return returnFormat(message='Gender already exists', status=400)

        gender = GenderModel(**data)

        gender.save_to_db()

        return returnFormat(message='Gender created succesfully', data=gender.json(), status=201)

    def get(self):

        data = GenderList.get_parser.parse_args()
        gender_list = GenderModel.find_by_attributes(**data)

        return returnFormat(message='Gender list retrieved succesfully', data=[gender.json() for gender in gender_list])

from flask_restful import Resource, reqparse

from models.age import AgeModel
from helpers.format import returnFormat


class Age(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')

    def get(self, id):

        age = AgeModel.find_by_id(id)
        if not age:
            return returnFormat(message='Age not found', status=404)

        return returnFormat(message='Age retrieved succesfully', data=age.json())

    def delete(self, id):

        age = AgeModel.find_by_id(id)
        if not age:
            return returnFormat(message='Age not found', status=404)

        age.delete_from_db()

        return returnFormat(message='Age deleted succesfully')

    def put(self, id):

        data = Age.put_parser.parse_args()

        age = AgeModel.find_by_id(id)
        if not age:
            return returnFormat(message='Age not found', status=404)

        if AgeModel.find_by_name(data['name']) and age.name != data['name']:
            return returnFormat(message='Age already exists', status=400)

        age.name = data['name']

        age.save_to_db()

        return returnFormat(message='Age updated succesfully', data=age.json())


class AgeList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of age to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of age to retrive', location='args')

    def post(self):

        data = AgeList.post_parser.parse_args()

        if AgeModel.find_by_name(data['name']):
            return returnFormat(message='Age already exists', status=400)

        age = AgeModel(**data)

        age.save_to_db()

        return returnFormat(message='Age created succesfully', data=age.json(), status=201)

    def get(self):

        data = AgeList.get_parser.parse_args()
        age_list = AgeModel.find_by_attributes(**data)

        return returnFormat(message='Age list retrieved succesfully', data=[age.json() for age in age_list])

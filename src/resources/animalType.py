from flask_restful import Resource, reqparse

from models.animalType import AnimalTypeModel
from helpers.format import returnFormat


class AnimalType(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')

    def get(self, id):

        animalType = AnimalTypeModel.find_by_id(id)
        if not animalType:
            return returnFormat(message='AnimalType not found', status=404)

        return returnFormat(message='AnimalType retrieved succesfully', data=animalType.json())

    def delete(self, id):

        animalType = AnimalTypeModel.find_by_id(id)
        if not animalType:
            return returnFormat(message='AnimalType not found', status=404)

        animalType.delete_from_db()

        return returnFormat(message='AnimalType deleted succesfully')

    def put(self, id):

        data = AnimalType.put_parser.parse_args()

        animalType = AnimalTypeModel.find_by_id(id)
        if not animalType:
            return returnFormat(message='AnimalType not found', status=404)

        if AnimalTypeModel.find_by_name(data['name']) and animalType.name != data['name']:
            return returnFormat(message='AnimalType already exists', status=400)

        animalType.name = data['name']

        animalType.save_to_db()

        return returnFormat(message='AnimalType updated succesfully', data=animalType.json())


class AnimalTypeList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('name', type=str, required=False,
                            help='Name must be a valid string', location='args')
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of animalType to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of animalType to retrive', location='args')

    def post(self):

        data = AnimalTypeList.post_parser.parse_args()

        if AnimalTypeModel.find_by_name(data['name']):
            return returnFormat(message='AnimalType already exists', status=400)

        animalType = AnimalTypeModel(**data)

        animalType.save_to_db()

        return returnFormat(message='AnimalType created succesfully', data=animalType.json(), status=201)

    def get(self):

        data = AnimalTypeList.get_parser.parse_args()
        animalType_list = AnimalTypeModel.find_by_attributes(**data)

        return returnFormat(message='AnimalType list retrieved succesfully', data=[animalType.json() for animalType in animalType_list])

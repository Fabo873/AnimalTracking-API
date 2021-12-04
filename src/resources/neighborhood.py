from flask_restful import Resource, reqparse

from models.neighborhood import NeighborhoodModel
from models.municipality import MunicipalityModel
from helpers.format import returnFormat


class Neighborhood(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')
    put_parser.add_argument('municipality_id', type=int, required=True,
                            help='municipality_id is an required param', location='json')

    def get(self, id):

        neighborhood = NeighborhoodModel.find_by_id(id)
        if not neighborhood:
            return returnFormat(message='Neighborhood not found', status=404)

        return returnFormat(message='Neighborhood retrieved succesfully', data=neighborhood.json())

    def delete(self, id):

        neighborhood = NeighborhoodModel.find_by_id(id)
        if not neighborhood:
            return returnFormat(message='Neighborhood not found', status=404)

        neighborhood.delete_from_db()

        return returnFormat(message='Neighborhood deleted succesfully')

    def put(self, id):

        data = Neighborhood.put_parser.parse_args()

        neighborhood = NeighborhoodModel.find_by_id(id)
        if not neighborhood:
            return returnFormat(message='Neighborhood not found', status=404)

        municipality = MunicipalityModel.find_by_id(data['municipality_id'])
        if not municipality:
            return returnFormat(message='Municipality not found', status=404)

        if NeighborhoodModel.find_by_attributes(name=data['name'], municipality_id=data['municipality_id']):
            if neighborhood.name != data['name'] or neighborhood.municipality_id != data['municipality_id']:
                return returnFormat(message='Neighborhood already exists', status=400)

        neighborhood.name = data['name']
        neighborhood.municipality_id = data['municipality_id']

        neighborhood.save_to_db()

        return returnFormat(message='Neighborhood updated succesfully', data=neighborhood.json())


class NeighborhoodList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')
    post_parser.add_argument('municipality_id', type=int, required=True,
                             help='municipality_id is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('name', type=str, required=False,
                            help='Name must be a valid string', location='args')
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of municipalities to retrice', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of municipalities to retrice', location='args')
    get_parser.add_argument('municipality_id', type=int, required=False,
                            help='municipality_id of municipalities to retrice', location='args')

    def post(self):

        data = NeighborhoodList.post_parser.parse_args()

        if NeighborhoodModel.find_by_attributes(name=data['name'], municipality_id=data['municipality_id']):
            return returnFormat(message='Neighborhood already exists', status=400)

        municipality = MunicipalityModel.find_by_id(data['municipality_id'])
        if not municipality:
            return returnFormat(message='Municipality not found', status=404)

        neighborhood = NeighborhoodModel(**data)
        neighborhood.save_to_db()

        return returnFormat(message='Neighborhood created succesfully', data=neighborhood.json(), status=201)

    def get(self):

        data = NeighborhoodList.get_parser.parse_args()
        print(data)
        municipalities = NeighborhoodModel.find_by_attributes(**data)
        return returnFormat(message='Neighborhood list retrieved succesfully', data=[neighborhood.json() for neighborhood in municipalities])

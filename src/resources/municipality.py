from flask_restful import Resource, reqparse

from models.municipality import MunicipalityModel
from helpers.format import returnFormat


class Municipality(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')
    put_parser.add_argument('state_id', type=int, required=True,
                            help='state_id is an required param', location='json')

    def get(self, id):

        municipality = MunicipalityModel.find_by_id(id)
        if not municipality:
            return returnFormat(message='Municipality not found', status=404)

        return returnFormat(message='Municipality retrieved succesfully', data=municipality.json())

    def delete(self, id):

        municipality = MunicipalityModel.find_by_id(id)
        if not municipality:
            return returnFormat(message='Municipality not found', status=404)

        municipality.delete_from_db()

        return returnFormat(message='Municipality deleted succesfully')

    def put(self, id):

        data = Municipality.put_parser.parse_args()

        municipality = MunicipalityModel.find_by_id(id)
        if not municipality:
            return returnFormat(message='Municipality not found', status=404)

        municipality.name = data['name']
        municipality.state_id = data['state_id']

        municipality.save_to_db()

        return returnFormat(message='Municipality updated succesfully', data=municipality.json())


class MunicipalityList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')
    post_parser.add_argument('state_id', type=int, required=True,
                             help='state_id is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of municipalities to retrice', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of municipalities to retrice', location='args')
    get_parser.add_argument('state_id', type=int, required=False,
                            help='state_id of municipalities to retrice', location='args')

    def post(self):

        data = MunicipalityList.post_parser.parse_args()

        if MunicipalityModel.find_by_attributes(name=data['name'], state_id=data['state_id']):
            return returnFormat(message='Municipality already exists', status=400)

        municipality = MunicipalityModel(**data)
        municipality.save_to_db()

        return returnFormat(message='Municipality created succesfully', data=municipality.json(), status=201)

    def get(self):

        data = MunicipalityList.get_parser.parse_args()
        municipalities = MunicipalityModel.find_by_attributes(**data)
        return returnFormat(message='Municipality list retrieved succesfully', data=[municipality.json() for municipality in municipalities])

from flask_restful import Resource, reqparse

from models.location import LocationModel
from models.municipality import MunicipalityModel
from helpers.format import returnFormat


class Location(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')
    put_parser.add_argument('municipality_id', type=int, required=True,
                            help='municipality_id is an required param', location='json')
    put_parser.add_argument('type', type=str, required=False,
                            help='type of the location', location='json')
    put_parser.add_argument('lat', type=float, required=False,
                            help='latitude of the location', location='json')
    put_parser.add_argument('lon', type=float, required=False,
                            help='longitude of the location', location='json')
    put_parser.add_argument('altitude', type=int, required=False,
                            help='altitude of the location', location='json')

    def get(self, id):

        location = LocationModel.find_by_id(id)
        if not location:
            return returnFormat(message='Location not found', status=404)

        return returnFormat(message='Location retrieved succesfully', data=location.json())

    def delete(self, id):

        location = LocationModel.find_by_id(id)
        if not location:
            return returnFormat(message='Location not found', status=404)

        location.delete_from_db()

        return returnFormat(message='Location deleted succesfully')

    def put(self, id):

        data = Location.put_parser.parse_args()

        location = LocationModel.find_by_id(id)
        if not location:
            return returnFormat(message='Location not found', status=404)

        municipality = MunicipalityModel.find_by_id(data['municipality_id'])
        if not municipality:
            return returnFormat(message='Municipality not found', status=404)

        location.name = data['name']
        location.municipality_id = data['municipality_id']
        location.type = data['type']
        location.lat = data['lat']
        location.lon = data['lon']
        location.altitude = data['altitude']

        location.save_to_db()

        return returnFormat(message='Location updated succesfully', data=location.json())


class LocationList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')
    post_parser.add_argument('municipality_id', type=int, required=True,
                             help='municipality_id is an required param', location='json')
    post_parser.add_argument('type', type=str, required=False,
                             help='type of the location', location='json')
    post_parser.add_argument('lat', type=float, required=False,
                             help='latitude of the location', location='json')
    post_parser.add_argument('lon', type=float, required=False,
                             help='longitude of the location', location='json')
    post_parser.add_argument('altitude', type=int, required=False,
                             help='altitude of the location', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of municipalities to retrice', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of municipalities to retrice', location='args')
    get_parser.add_argument('municipality_id', type=int, required=False,
                            help='municipality_id of municipalities to retrice', location='args')
    get_parser.add_argument('type', type=str, required=False,
                            help='type of the location', location='args')

    def post(self):

        data = LocationList.post_parser.parse_args()

        if LocationModel.find_by_attributes(name=data['name'], municipality_id=data['municipality_id']):
            return returnFormat(message='Location already exists', status=400)

        municipality = MunicipalityModel.find_by_id(data['municipality_id'])
        if not municipality:
            return returnFormat(message='Municipality not found', status=404)

        location = LocationModel(**data)
        location.save_to_db()

        return returnFormat(message='Location created succesfully', data=location.json(), status=201)

    def get(self):

        data = LocationList.get_parser.parse_args()
        print(data)
        municipalities = LocationModel.find_by_attributes(**data)
        return returnFormat(message='Location list retrieved succesfully', data=[location.json() for location in municipalities])

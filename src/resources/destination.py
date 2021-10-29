from flask_restful import Resource, reqparse

from models.destination import DestinationModel
from helpers.format import returnFormat


class Destination(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')

    def get(self, id):

        destination = DestinationModel.find_by_id(id)
        if not destination:
            return returnFormat(message='Destination not found', status=404)

        return returnFormat(message='Destination retrieved succesfully', data=destination.json())

    def delete(self, id):

        destination = DestinationModel.find_by_id(id)
        if not destination:
            return returnFormat(message='Destination not found', status=404)

        destination.delete_from_db()

        return returnFormat(message='Destination deleted succesfully')

    def put(self, id):

        data = Destination.put_parser.parse_args()

        destination = DestinationModel.find_by_id(id)
        if not destination:
            return returnFormat(message='Destination not found', status=404)

        if DestinationModel.find_by_name(data['name']) and destination.name != data['name']:
            return returnFormat(message='Destination already exists', status=400)

        destination.name = data['name']

        destination.save_to_db()

        return returnFormat(message='Destination updated succesfully', data=destination.json())


class DestinationList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of destination to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of destination to retrive', location='args')

    def post(self):

        data = DestinationList.post_parser.parse_args()

        if DestinationModel.find_by_name(data['name']):
            return returnFormat(message='Destination already exists', status=400)

        destination = DestinationModel(**data)

        destination.save_to_db()

        return returnFormat(message='Destination created succesfully', data=destination.json(), status=201)

    def get(self):

        data = DestinationList.get_parser.parse_args()
        destination_list = DestinationModel.find_by_attributes(**data)

        return returnFormat(message='Destination list retrieved succesfully', data=[destination.json() for destination in destination_list])

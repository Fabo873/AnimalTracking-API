from flask_restful import Resource, reqparse

from models.state import StateModel
from helpers.format import returnFormat


class State(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=str, required=True,
                            help='Name is an required param', location='json')
    put_parser.add_argument('initials', type=str, required=True,
                            help='initials is an required param', location='json')

    def get(self, id):

        state = StateModel.find_by_id(id)
        if not state:
            return returnFormat(message='State not found', status=404)

        return returnFormat(message='State retrieved succesfully', data=state.json())

    def delete(self, id):

        state = StateModel.find_by_id(id)
        if not state:
            return returnFormat(message='State not found', status=404)

        state.delete_from_db()

        return returnFormat(message='State deleted succesfully')

    def put(self, id):

        data = State.put_parser.parse_args()

        state = StateModel.find_by_id(id)
        if not state:
            return returnFormat(message='State not found', status=404)

        if StateModel.find_by_name(data['name']) and state.name != data['name']:
            return returnFormat(message='State already exists', status=400)

        state.name = data['name']
        state.initials = data['initials']

        state.save_to_db()

        return returnFormat(message='State updated succesfully', data=state.json())


class StateList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True,
                             help='Name is an required param', location='json')
    post_parser.add_argument('initials', type=str, required=True,
                             help='initials is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of states to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of states to retrive', location='args')

    def post(self):

        data = StateList.post_parser.parse_args()

        if StateModel.find_by_name(data['name']):
            return returnFormat(message='State already exists', status=400)

        state = StateModel(**data)

        state.save_to_db()

        return returnFormat(message='State created succesfully', data=state.json(), status=201)

    def get(self):

        data = StateList.get_parser.parse_args()
        states = StateModel.find_by_attributes(**data)

        return returnFormat(message='State list retrieved succesfully', data=[state.json() for state in states])

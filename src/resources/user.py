from flask_restful import Resource, reqparse
from helpers.encryption import Encryption

from models.user import UserModel
from helpers.format import returnFormat


class User(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('username', type=str, required=True,
                            help='Name is an required param', location='json')
    put_parser.add_argument('password', type=str, required=True,
                            help='password is an required param', location='json')

    def get(self, id):

        user = UserModel.find_by_id(id)
        if not user:
            return returnFormat(message='User not found', status=404)

        return returnFormat(message='User retrieved succesfully', data=user.json())

    def delete(self, id):

        user = UserModel.find_by_id(id)
        if not user:
            return returnFormat(message='User not found', status=404)

        user.delete_from_db()

        return returnFormat(message='User deleted succesfully')

    def put(self, id):

        data = User.put_parser.parse_args()

        user = UserModel.find_by_id(id)
        if not user:
            return returnFormat(message='User not found', status=404)

        if UserModel.find_by_username(data['username']) and user.username != data['username']:
            return returnFormat(message='User already exists', status=400)

        user.username = data['username']
        user.password = Encryption.encode(data['password'])

        user.save_to_db()

        return returnFormat(message='User updated succesfully', data=user.json())


class UserList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('username', type=str, required=True,
                             help='Name is an required param', location='json')
    post_parser.add_argument('password', type=str, required=True,
                             help='password is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of users to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of users to retrive', location='args')

    def post(self):

        data = UserList.post_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return returnFormat(message='User already exists', status=400)

        user = UserModel(**data)

        user.save_to_db()

        return returnFormat(message='User created succesfully', data=user.json(), status=201)

    def get(self):

        data = UserList.get_parser.parse_args()
        users = UserModel.find_by_attributes(**data)

        return returnFormat(message='User list retrieved succesfully', data=[user.json() for user in users])

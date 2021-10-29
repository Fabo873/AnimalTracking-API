from flask_restful import Resource, reqparse
from models.location import LocationModel

from models.reception import ReceptionModel
from models.person import PersonModel
from helpers.format import returnFormat
from models.specimen import SpecimenModel


class Reception(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('deliver_person', type=str, required=False,
                            help='deliver_person is an required param', location='json')
    put_parser.add_argument('reciever_person_id', type=int, required=True,
                            help='reciever_person_id is an required param', location='json')
    put_parser.add_argument('specimen_id', type=int, required=True,
                            help='specimen_id is an required param', location='json')
    put_parser.add_argument('location_id', type=int, required=False,
                            help='location_id is an required param', location='json')

    def get(self, id):

        reception = ReceptionModel.find_by_id(id)
        if not reception:
            return returnFormat(message='Reception not found', status=404)

        return returnFormat(message='Reception retrieved succesfully', data=reception.json())

    def delete(self, id):

        reception = ReceptionModel.find_by_id(id)
        if not reception:
            return returnFormat(message='Reception not found', status=404)

        reception.delete_from_db()

        return returnFormat(message='Reception deleted succesfully')

    def put(self, id):

        data = Reception.put_parser.parse_args()

        reception = ReceptionModel.find_by_id(id)
        if not reception:
            return returnFormat(message='Reception not found', status=404)

        if ReceptionModel.find_by_specimen_id(data['specimen_id']) and data['specimen_id'] != reception.specimen_id:
            return returnFormat(message='specimen already asigned to reception', status=400)

        specimen = SpecimenModel.find_by_id(data['specimen_id'])
        if not specimen:
            return returnFormat(message='specimen not found', status=404)

        location = LocationModel.find_by_id(data['location_id'])
        if not location:
            return returnFormat(message='location not found', status=404)

        person = PersonModel.find_by_id(data['reciever_person_id'])
        if not person:
            return returnFormat(message='person not found', status=404)

        reception.deliver_person = data['deliver_person']
        reception.specimen_id = data['specimen_id']
        reception.location_id = data['location_id']
        reception.reciever_person_id = data['reciever_person_id']

        reception.save_to_db()

        return returnFormat(message='Reception updated succesfully', data=reception.json())


class ReceptionList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('deliver_person', type=str, required=False,
                             help='deliver_person is an required param', location='json')
    post_parser.add_argument('reciever_person_id', type=int, required=True,
                             help='reciever_person_id is an required param', location='json')
    post_parser.add_argument('specimen_id', type=int, required=True,
                             help='specimen_id is an required param', location='json')
    post_parser.add_argument('location_id', type=int, required=False,
                             help='location_id is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of reception to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of reception to retrive', location='args')
    get_parser.add_argument('reciever_person_id', type=int, required=False,
                            help='reciever_person_id is an required param', location='args')
    get_parser.add_argument('specimen_id', type=int, required=False,
                            help='specimen_id is an required param', location='args')
    get_parser.add_argument('location_id', type=int, required=False,
                            help='location_id is an required param', location='args')

    def post(self):

        data = ReceptionList.post_parser.parse_args()

        reception = ReceptionModel.find_by_specimen_id(data['specimen_id'])
        if reception:
            return returnFormat(message='specimen already asigned to reception', status=400)

        specimen = SpecimenModel.find_by_id(data['specimen_id'])
        if not specimen:
            return returnFormat(message='specimen not found', status=404)

        location = LocationModel.find_by_id(data['location_id'])
        if not location:
            return returnFormat(message='location not found', status=404)

        person = PersonModel.find_by_id(data['reciever_person_id'])
        if not person:
            return returnFormat(message='person not found', status=404)

        reception = ReceptionModel(**data)

        reception.save_to_db()

        return returnFormat(message='Reception created succesfully', data=reception.json(), status=201)

    def get(self):

        data = ReceptionList.get_parser.parse_args()
        reception_list = ReceptionModel.find_by_attributes(**data)

        return returnFormat(message='Reception list retrieved succesfully', data=[reception.json() for reception in reception_list])

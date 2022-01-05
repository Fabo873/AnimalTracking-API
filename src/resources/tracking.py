from flask_restful import Resource, reqparse
from flask import make_response
from models.destination import DestinationModel

from models.tracking import TrackingModel
from models.destination import DestinationModel
from helpers.format import returnFormat, toCsv
from models.specimen import SpecimenModel

from datetime import datetime


class Tracking(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('condition', type=str, required=False,
                            help='condition must be a string', location='json')
    put_parser.add_argument('destination_id', type=int, required=True,
                            help='destination_id is an required param', location='json')
    put_parser.add_argument('specimen_id', type=int, required=True,
                            help='specimen_id is an required param', location='json')
    put_parser.add_argument('weigth', type=int, required=False,
                            help='weigth must be a float', location='json')
    put_parser.add_argument('size', type=int, required=False,
                            help='size must be a float', location='json')
    put_parser.add_argument('reviewed', type=bool, required=False,
                            help='reviewed must be a bool', location='json')
    put_parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                            help='date is required (dd-mm-yy)', location='json')

    def get(self, id):

        tracking = TrackingModel.find_by_id(id)
        if not tracking:
            return returnFormat(message='Tracking not found', status=404)

        return returnFormat(message='Tracking retrieved succesfully', data=tracking.json())

    def delete(self, id):

        tracking = TrackingModel.find_by_id(id)
        if not tracking:
            return returnFormat(message='Tracking not found', status=404)

        tracking.delete_from_db()

        return returnFormat(message='Tracking deleted succesfully')

    def put(self, id):

        data = Tracking.put_parser.parse_args()

        tracking = TrackingModel.find_by_id(id)
        if not tracking:
            return returnFormat(message='Tracking not found', status=404)

        specimen = SpecimenModel.find_by_id(data['specimen_id'])
        if not specimen:
            return returnFormat(message='specimen not found', status=404)

        destination = DestinationModel.find_by_id(data['destination_id'])
        if not destination:
            return returnFormat(message='destination not found', status=404)

        tracking.condition = data['condition']
        tracking.specimen_id = data['specimen_id']
        tracking.weigth = data['weigth']
        tracking.size = data['size']
        tracking.destination_id = data['destination_id']
        tracking.reviewed = data['reviewed']

        tracking.save_to_db()

        return returnFormat(message='Tracking updated succesfully', data=tracking.json())


class TrackingList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('specimen_id', type=int, required=True,
                             help='specimen_id is an required param', location='json')
    post_parser.add_argument('condition', type=str, required=False,
                             help='condition must be a string', location='json')
    post_parser.add_argument('destination_id', type=int, required=True,
                             help='destination_id is an required param', location='json')
    post_parser.add_argument('weigth', type=int, required=False,
                             help='weigth must be a float', location='json')
    post_parser.add_argument('size', type=int, required=False,
                             help='size must be a float', location='json')
    post_parser.add_argument('reviewed', type=bool, required=False,
                             help='reviewed must be a bool', location='json')
    post_parser.add_argument('date', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of tracking to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of tracking to retrive', location='args')
    get_parser.add_argument('person_id', type=int, required=False,
                            help='person_id is an required param', location='args')
    get_parser.add_argument('animalType_id', type=int, required=False,
                            help='animalType_id is an required param', location='args')
    get_parser.add_argument('species_id', type=int, required=False,
                            help='species_id is an required param', location='args')
    get_parser.add_argument('age_id', type=int, required=False,
                            help='age_id is an required param', location='args')
    get_parser.add_argument('folio', type=str, required=False,
                            help='folio is an required param', location='args')
    get_parser.add_argument('gender_id', type=int, required=False,
                            help='gender_id is an required param', location='args')
    get_parser.add_argument('destination_id', type=int, required=False,
                            help='destination_id is an required param', location='args')
    get_parser.add_argument('specimen_id', type=int, required=False,
                            help='specimen_id is an required param', location='args')
    get_parser.add_argument('reviewed', type=bool, required=False,
                            help='reviewed is a bool param', location='args')
    get_parser.add_argument('date_from', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')
    get_parser.add_argument('date_to', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')

    def post(self):

        data = TrackingList.post_parser.parse_args()

        print(data)

        specimen = SpecimenModel.find_by_id(data['specimen_id'])
        if not specimen:
            return returnFormat(message='specimen not found', status=404)

        destination = DestinationModel.find_by_id(data['destination_id'])
        if not destination:
            return returnFormat(message='destination not found', status=404)

        tracking = TrackingModel(**data)

        tracking.save_to_db()

        return returnFormat(message='Tracking created succesfully', data=tracking.json(), status=201)

    def get(self):

        data = TrackingList.get_parser.parse_args()
        tracking_list = TrackingModel.find_by_attributes(**data)

        return returnFormat(message='Tracking list retrieved succesfully', data=[tracking.json() for tracking in tracking_list])

class TrackingCSV(Resource):

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of tracking to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of tracking to retrive', location='args')
    get_parser.add_argument('person_id', type=int, required=False,
                            help='person_id is an required param', location='args')
    get_parser.add_argument('animalType_id', type=int, required=False,
                            help='animalType_id is an required param', location='args')
    get_parser.add_argument('species_id', type=int, required=False,
                            help='species_id is an required param', location='args')
    get_parser.add_argument('age_id', type=int, required=False,
                            help='age_id is an required param', location='args')
    get_parser.add_argument('folio', type=str, required=False,
                            help='folio is an required param', location='args')
    get_parser.add_argument('gender_id', type=int, required=False,
                            help='gender_id is an required param', location='args')
    get_parser.add_argument('destination_id', type=int, required=False,
                            help='destination_id is an required param', location='args')
    get_parser.add_argument('specimen_id', type=int, required=False,
                            help='specimen_id is an required param', location='args')
    get_parser.add_argument('reviewed', type=bool, required=False,
                            help='reviewed is a bool param', location='args')
    get_parser.add_argument('date_from', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')
    get_parser.add_argument('date_to', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')

    def get(self):

        data = TrackingList.get_parser.parse_args()
        tracking_list = TrackingModel.find_by_attributes(**data)
        labels = TrackingModel.getCsvLabels()
        rows = [tracking.csv() for tracking in tracking_list]
        response = make_response(toCsv(labels, rows))
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=scpecimens.csv'

        return response
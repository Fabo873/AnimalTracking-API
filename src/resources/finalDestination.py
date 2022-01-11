from datetime import datetime
from flask_restful import Resource, reqparse
from flask import make_response
from models.destination import DestinationModel

from models.finalDestination import FinalDestinationModel
from models.destination import DestinationModel
from helpers.format import returnFormat, toCsv
from models.specimen import SpecimenModel


class FinalDestination(Resource):

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
    put_parser.add_argument('notes', type=str, required=False,
                            help='notes must be a string', location='json')

    def get(self, id):

        finalDestination = FinalDestinationModel.find_by_id(id)
        if not finalDestination:
            return returnFormat(message='FinalDestination not found', status=404)

        return returnFormat(message='FinalDestination retrieved succesfully', data=finalDestination.json())

    def delete(self, id):

        finalDestination = FinalDestinationModel.find_by_id(id)
        if not finalDestination:
            return returnFormat(message='FinalDestination not found', status=404)

        finalDestination.delete_from_db()

        return returnFormat(message='FinalDestination deleted succesfully')

    def put(self, id):

        data = FinalDestination.put_parser.parse_args()

        finalDestination = FinalDestinationModel.find_by_id(id)
        if not finalDestination:
            return returnFormat(message='FinalDestination not found', status=404)

        if FinalDestinationModel.find_by_specimen_id(data['specimen_id']) and data['specimen_id'] != finalDestination.specimen_id:
            return returnFormat(message='specimen already asigned to finalDestination', status=400)

        specimen = SpecimenModel.find_by_id(data['specimen_id'])
        if not specimen:
            return returnFormat(message='specimen not found', status=404)

        destination = DestinationModel.find_by_id(data['destination_id'])
        if not destination:
            return returnFormat(message='destination not found', status=404)

        finalDestination.condition = data['condition']
        finalDestination.specimen_id = data['specimen_id']
        finalDestination.weigth = data['weigth']
        finalDestination.size = data['size']
        finalDestination.destination_id = data['destination_id']
        finalDestination.notes = data['notes']

        finalDestination.save_to_db()

        return returnFormat(message='FinalDestination updated succesfully', data=finalDestination.json())


class FinalDestinationList(Resource):

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
    post_parser.add_argument('notes', type=str, required=False,
                             help='notes must be a string', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of finalDestination to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of finalDestination to retrive', location='args')
    get_parser.add_argument('destination_id', type=int, required=False,
                            help='destination_id is an required param', location='args')
    get_parser.add_argument('specimen_id', type=int, required=False,
                            help='specimen_id is an required param', location='args')
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
    get_parser.add_argument('date_from', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')
    get_parser.add_argument('date_to', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')
    
    def post(self):

        data = FinalDestinationList.post_parser.parse_args()

        finalDestination = FinalDestinationModel.find_by_specimen_id(
            data['specimen_id'])
        if finalDestination:
            return returnFormat(message='specimen already asigned to finalDestination', status=400)

        specimen = SpecimenModel.find_by_id(data['specimen_id'])
        if not specimen:
            return returnFormat(message='specimen not found', status=404)

        destination = DestinationModel.find_by_id(data['destination_id'])
        if not destination:
            return returnFormat(message='destination not found', status=404)

        finalDestination = FinalDestinationModel(**data)

        finalDestination.save_to_db()

        return returnFormat(message='FinalDestination created succesfully', data=finalDestination.json(), status=201)

    def get(self):

        data = FinalDestinationList.get_parser.parse_args()
        finalDestination_list = FinalDestinationModel.find_by_attributes(
            **data)

        return returnFormat(message='FinalDestination list retrieved succesfully', data=[finalDestination.json() for finalDestination in finalDestination_list])

class FinalDestinationCSV(Resource):

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of finalDestination to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of finalDestination to retrive', location='args')
    get_parser.add_argument('destination_id', type=int, required=False,
                            help='destination_id is an required param', location='args')
    get_parser.add_argument('specimen_id', type=int, required=False,
                            help='specimen_id is an required param', location='args')
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
    get_parser.add_argument('date_from', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')
    get_parser.add_argument('date_to', type=lambda x: datetime.strptime(x, '%d-%m-%y'), required=False,
                             help='date is required (dd-mm-yy)', location='args')

    def get(self):

        data = FinalDestinationList.get_parser.parse_args()
        finalDestination_list = FinalDestinationModel.find_by_attributes(
            **data)
        labels = FinalDestinationModel.getCsvLabels()
        rows = [finalDestination.csv() for finalDestination in finalDestination_list]
        response = make_response(toCsv(labels, rows))
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=final_destination.csv'

        return response
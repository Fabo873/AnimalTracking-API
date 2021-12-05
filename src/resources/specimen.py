import datetime
from flask_restful import Resource, reqparse
from models.age import AgeModel
from models.animalType import AnimalTypeModel
from models.destination import DestinationModel
from models.gender import GenderModel
from models.species import SpeciesModel

from models.specimen import SpecimenModel
from models.person import PersonModel
from helpers.format import returnFormat, folioFormat


class Specimen(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('animalType_id', type=int, required=True,
                            help='animalType_id is an required param', location='json')
    put_parser.add_argument('species_id', type=int, required=True,
                            help='species_id is an required param', location='json')
    put_parser.add_argument('age_id', type=int, required=True,
                            help='age_id is an required param', location='json')
    put_parser.add_argument('gender_id', type=int, required=True,
                            help='gender_id is an required param', location='json')
    put_parser.add_argument('destination_id', type=int, required=True,
                            help='destination_id is an required param', location='json')
    put_parser.add_argument('condition', type=str, required=False,
                            help='condition is an required param', location='json')
    put_parser.add_argument('weigth', type=float, required=False,
                            help='weigth must be a float', location='json')
    put_parser.add_argument('size', type=float, required=False,
                            help='size must be a float', location='json')

    def get(self, id):

        specimen = SpecimenModel.find_by_id(id)
        if not specimen:
            return returnFormat(message='Specimen not found', status=404)

        return returnFormat(message='Specimen retrieved succesfully', data=specimen.json())

    def delete(self, id):

        specimen = SpecimenModel.find_by_id(id)
        if not specimen:
            return returnFormat(message='Specimen not found', status=404)

        specimen.delete_from_db()

        return returnFormat(message='Specimen deleted succesfully')

    def put(self, id):

        data = Specimen.put_parser.parse_args()

        specimen = SpecimenModel.find_by_id(id)
        if not specimen:
            return returnFormat(message='Specimen not found', status=404)

        animalType = AnimalTypeModel.find_by_id(data['animalType_id'])
        if not animalType:
            return returnFormat(message='AnimalType not found', status=404)

        species = SpeciesModel.find_by_id(data['species_id'])
        if not species:
            return returnFormat(message='Species not found', status=404)

        age = AgeModel.find_by_id(data['age_id'])
        if not age:
            return returnFormat(message='Age not found', status=404)

        gender = GenderModel.find_by_id(data['gender_id'])
        if not gender:
            return returnFormat(message='Gender not found', status=404)

        destination = DestinationModel.find_by_id(data['destination_id'])
        if not destination:
            return returnFormat(message='Destination not found', status=404)

        specimen.animalType_id = data['animalType_id']
        specimen.species_id = data['species_id']
        specimen.age_id = data['age_id']
        specimen.gender_id = data['gender_id']
        specimen.destination_id = data['destination_id']
        specimen.condition = data['condition']
        specimen.weigth = data['weigth']
        specimen.size = data['size']

        specimen.save_to_db()

        return returnFormat(message='Specimen updated succesfully', data=specimen.json())


class SpecimenList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('person_id', type=int, required=True,
                             help='person_id is an required param', location='json')
    post_parser.add_argument('animalType_id', type=int, required=True,
                             help='animalType_id is an required param', location='json')
    post_parser.add_argument('species_id', type=int, required=True,
                             help='species_id is an required param', location='json')
    post_parser.add_argument('age_id', type=int, required=True,
                             help='age_id is an required param', location='json')
    post_parser.add_argument('gender_id', type=int, required=True,
                             help='gender_id is an required param', location='json')
    post_parser.add_argument('destination_id', type=int, required=True,
                             help='destination_id is an required param', location='json')
    post_parser.add_argument('condition', type=str, required=False,
                             help='condition is an required param', location='json')
    post_parser.add_argument('weigth', type=float, required=False,
                             help='weigth must be a float', location='json')
    post_parser.add_argument('size', type=float, required=False,
                             help='size must be a float', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of specimen to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of specimen to retrive', location='args')
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

    def post(self):

        data = SpecimenList.post_parser.parse_args()

        person = PersonModel.find_by_id(data['person_id'])
        if not person:
            return returnFormat(message='Person not found', status=404)

        animalType = AnimalTypeModel.find_by_id(data['animalType_id'])
        if not animalType:
            return returnFormat(message='AnimalType not found', status=404)

        species = SpeciesModel.find_by_id(data['species_id'])
        if not species:
            return returnFormat(message='Species not found', status=404)

        age = AgeModel.find_by_id(data['age_id'])
        if not age:
            return returnFormat(message='Age not found', status=404)

        gender = GenderModel.find_by_id(data['gender_id'])
        if not gender:
            return returnFormat(message='Gender not found', status=404)

        destination = DestinationModel.find_by_id(data['destination_id'])
        if not destination:
            return returnFormat(message='Destination not found', status=404)

        folio = folioFormat(datetime.date.today(), (SpecimenModel.get_specimen_day(
            person.id)+1), person.name, person.first_lastname, person.second_lastname)

        specimen = SpecimenModel(folio=folio, **data)

        specimen.save_to_db()

        return returnFormat(message='Specimen created succesfully', data=specimen.json(), status=201)

    def get(self):

        data = SpecimenList.get_parser.parse_args()
        specimen_list = SpecimenModel.find_by_attributes(**data)

        return returnFormat(message='Specimen list retrieved succesfully', data=[specimen.json() for specimen in specimen_list])

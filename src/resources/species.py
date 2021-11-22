from flask_restful import Resource, reqparse
from models.animalType import AnimalTypeModel

from models.species import SpeciesModel
from helpers.format import returnFormat


class Species(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('common_name', type=str, required=True,
                            help='Common Name is an required param', location='json')
    put_parser.add_argument('scientific_name', type=str, required=True,
                            help='Scientific Name is an required param', location='json')
    put_parser.add_argument('animal_type_id', type=str, required=True,
                            help='Animal Type Id is an required param', location='json')

    def get(self, id):

        species = SpeciesModel.find_by_id(id)
        if not species:
            return returnFormat(message='Species not found', status=404)

        return returnFormat(message='Species retrieved succesfully', data=species.json())

    def delete(self, id):

        species = SpeciesModel.find_by_id(id)
        if not species:
            return returnFormat(message='Species not found', status=404)

        species.delete_from_db()

        return returnFormat(message='Species deleted succesfully')

    def put(self, id):

        data = Species.put_parser.parse_args()

        species = SpeciesModel.find_by_id(id)
        if not species:
            return returnFormat(message='Species not found', status=404)

        if SpeciesModel.find_by_name(data['common_name']) and species.common_name != data['common_name']:
            return returnFormat(message='Species already exists', status=400)

        if SpeciesModel.find_by_scientific_name(data['scientific_name']) and species.scientific_name != data['scientific_name']:
            return returnFormat(message='Species already exists', status=400)

        animalType = AnimalTypeModel.find_by_id(data['animal_type_id'])
        if not animalType:
            return returnFormat(message='Animal Type not found', status=404)

        species.common_name = data['common_name']
        species.scientific_name = data['scientific_name']
        species.animal_type_id = data['animal_type_id']

        species.save_to_db()

        return returnFormat(message='Species updated succesfully', data=species.json())


class SpeciesList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('common_name', type=str, required=True,
                             help='Common Name is an required param', location='json')
    post_parser.add_argument('scientific_name', type=str, required=True,
                             help='Scientific Name is an required param', location='json')
    post_parser.add_argument('animal_type_id', type=str, required=True,
                             help='Animal Type Id is an required param', location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('common_name', type=str, required=False,
                            help='Common Name must be a valid string', location='args')
    get_parser.add_argument('scientific_name', type=str, required=False,
                            help='Scientific Name must be a valid string', location='args')
    get_parser.add_argument('animal_type_id', type=str, required=False,
                            help='Animal Type Id must be a valid integer', location='args')
    get_parser.add_argument('limit', type=int, required=False,
                            help='Limit of species to retrive', location='args')
    get_parser.add_argument('offset', type=int, required=False,
                            help='Offset of species to retrive', location='args')

    def post(self):

        data = SpeciesList.post_parser.parse_args()

        if SpeciesModel.find_by_name(data['common_name']):
            return returnFormat(message='Species already exists', status=400)

        if SpeciesModel.find_by_scientific_name(data['scientific_name']):
            return returnFormat(message='Species already exists', status=400)

        animalType = AnimalTypeModel.find_by_id(data['animal_type_id'])
        if not animalType:
            return returnFormat(message='Animal Type not found', status=404)

        species = SpeciesModel(**data)

        species.save_to_db()

        return returnFormat(message='Species created succesfully', data=species.json(), status=201)

    def get(self):

        data = SpeciesList.get_parser.parse_args()
        species_list = SpeciesModel.find_by_attributes(**data)

        return returnFormat(message='Species list retrieved succesfully', data=[species.json() for species in species_list])

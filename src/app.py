import os

# from datetime import timedelta
from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT

from helpers.db import db
from resources.state import State, StateList
from resources.municipality import Municipality, MunicipalityList
from resources.location import Location, LocationList
from resources.user import User, UserList
from resources.person import Person, PersonList
from resources.species import Species, SpeciesList
from resources.animalType import AnimalType, AnimalTypeList
from resources.destination import Destination, DestinationList
from resources.gender import Gender, GenderList
from resources.age import Age, AgeList
from resources.specimen import Specimen, SpecimenList
from resources.reception import Reception, ReceptionList
from resources.finalDestination import FinalDestination, FinalDestinationList
from resources.tracking import Tracking, TrackingList

db_uri = 'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(db_user=os.environ['DB_USER'],
                                                                                        db_password=os.environ['DB_PASSWORD'],
                                                                                        db_host=os.environ['DB_HOST'],
                                                                                        db_port=os.environ['DB_PORT'],
                                                                                        db_name=os.environ['DB_NAME'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

api.add_resource(StateList, '/state')
api.add_resource(State, '/state/<int:id>')

api.add_resource(MunicipalityList, '/municipality')
api.add_resource(Municipality, '/municipality/<int:id>')

api.add_resource(LocationList, '/location')
api.add_resource(Location, '/location/<int:id>')

api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<int:id>')

api.add_resource(PersonList, '/person')
api.add_resource(Person, '/person/<int:id>')

api.add_resource(SpeciesList, '/species')
api.add_resource(Species, '/species/<int:id>')

api.add_resource(AnimalTypeList, '/type')
api.add_resource(AnimalType, '/type/<int:id>')

api.add_resource(DestinationList, '/destination')
api.add_resource(Destination, '/destination/<int:id>')

api.add_resource(GenderList, '/gender')
api.add_resource(Gender, '/gender/<int:id>')

api.add_resource(AgeList, '/age')
api.add_resource(Age, '/age/<int:id>')

api.add_resource(SpecimenList, '/specimen')
api.add_resource(Specimen, '/specimen/<int:id>')

api.add_resource(ReceptionList, '/reception')
api.add_resource(Reception, '/reception/<int:id>')

api.add_resource(FinalDestinationList, '/final')
api.add_resource(FinalDestination, '/final/<int:id>')

api.add_resource(TrackingList, '/tracking')
api.add_resource(Tracking, '/tracking/<int:id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(host=os.environ['API_HOST'], port=os.environ['API_PORT'], debug=True)

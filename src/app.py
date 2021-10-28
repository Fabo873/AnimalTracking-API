import os

from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from helpers.db import db
from resources.state import State, StateList
from resources.municipality import Municipality, MunicipalityList
from resources.location import Location, LocationList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://eduardo:eduardo@127.0.0.1:3306/REPORTS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

api.add_resource(StateList, '/state')
api.add_resource(State, '/state/<int:id>')

api.add_resource(MunicipalityList, '/municipality')
api.add_resource(Municipality, '/municipality/<int:id>')

api.add_resource(LocationList, '/location')
api.add_resource(Location, '/location/<int:id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)

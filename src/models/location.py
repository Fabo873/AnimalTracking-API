from __future__ import annotations

import flask
from helpers.db import db
from typing import List, Dict


class LocationModel(db.Model):
    __tablename__ = 'Locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(1))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    altitude = db.Column(db.Integer)
    municipality_id = db.Column(db.Integer, db.ForeignKey('Municipalities.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    municipality = db.relationship(
        'MunicipalityModel', back_populates="locations")

    def __init__(self, name: str, municipality_id: int, _id: int = None, type: str = None, lat: float = None, lon: float = None, altitude: int = None) -> None:
        self.id = _id
        self.name = name
        self.type = type
        self.lat = lat
        self.lon = lon
        self.altitude = altitude
        self.municipality_id = municipality_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id, 'name': self.name, 'type': self.type, 'lat': self.lat, 'lon': self.lon, 'altitude': self.altitude, 'municipality_id': self.municipality_id}

    @classmethod
    def find_by_attributes(cls, name: str = None, municipality_id: int = None, type: str = None, limit: int = None, offset: int = None) -> List:
        locations = cls.query
        if name:
            locations = locations.filter_by(name=name)
        if municipality_id:
            locations = locations.filter_by(municipality_id=municipality_id)
        if type:
            locations = locations.filter_by(type=type)
        if limit:
            locations = locations.limit(limit)
        if offset:
            locations = locations.offset(offset)
        return locations.all()

    @classmethod
    def find_by_id(cls, _id: int) -> LocationModel:
        return cls.query.filter_by(id=_id).first()

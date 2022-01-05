from __future__ import annotations

from helpers.db import db
from typing import List, Dict


class NeighborhoodModel(db.Model):
    __tablename__ = 'Neighborhoods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    municipality_id = db.Column(db.Integer, db.ForeignKey('Municipalities.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    municipality = db.relationship(
        'MunicipalityModel', back_populates="neighborhoods")

    def __init__(self, name: str, municipality_id: int, _id: int = None) -> None:
        self.id = _id
        self.name = name
        self.municipality_id = municipality_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> dict:
        return {'id': self.id, 'name': self.name, 'municipality': self.municipality.json()}

    @classmethod
    def find_by_attributes(cls, name: str = None, municipality_id: int = None, limit: int = None, offset: int = None) -> list:
        neighborhoods = cls.query
        if name:
            search = "%{}%".format(name)
            neighborhoods = neighborhoods.filter(cls.name.like(search))
        if municipality_id:
            neighborhoods = neighborhoods.filter_by(municipality_id=municipality_id)
        if limit:
            neighborhoods = neighborhoods.limit(limit)
        if offset:
            neighborhoods = neighborhoods.offset(offset)
        return neighborhoods.all()

    @classmethod
    def find_by_id(cls, _id: int) -> NeighborhoodModel:
        return cls.query.filter_by(id=_id).first()

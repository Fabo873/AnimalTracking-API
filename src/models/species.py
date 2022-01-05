from __future__ import annotations
from helpers.db import db
from typing import List, Dict
from sqlalchemy import func


class SpeciesModel(db.Model):
    __tablename__ = 'Species'

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100))
    animal_type_id = db.Column(db.Integer, db.ForeignKey('AnimalType.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    animal_type = db.relationship('AnimalTypeModel')

    def __init__(self, common_name: str, scientific_name: str, animal_type_id: int, _id: int = None) -> None:
        self.id = _id
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.animal_type_id = animal_type_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> dict:
        return {'id': self.id, 'common_name': self.common_name, 'scientific_name': self.scientific_name, 'animal_type': self.animal_type.json()}

    @classmethod
    def find_by_name(cls, common_name: str) -> SpeciesModel:
        return cls.query.filter(func.lower(cls.common_name) == func.lower(common_name)).first()

    @classmethod
    def find_by_scientific_name(cls, scientific_name: str) -> SpeciesModel:
        return cls.query.filter(func.lower(cls.scientific_name) == func.lower(scientific_name)).first()

    @classmethod
    def find_by_attributes(cls, common_name: str = None, scientific_name: str = None, limit: int = None, animal_type_id: int = None, offset: int = None) -> List:
        species = cls.query
        if common_name:
            search = "%{}%".format(common_name)
            species = species.filter(cls.common_name.like(search))
        if scientific_name:
            search = "%{}%".format(scientific_name)
            species = species.filter(cls.scientific_name.like(search))
        if animal_type_id:
            species = species.filter_by(animal_type_id=animal_type_id)
        if limit:
            species = species.limit(limit)
        if offset:
            species = species.offset(offset)
        return species.all()

    @classmethod
    def find_by_id(cls, _id: int) -> SpeciesModel:
        return cls.query.filter_by(id=_id).first()

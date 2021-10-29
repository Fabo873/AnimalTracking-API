from __future__ import annotations
from helpers.db import db
from typing import List, Dict


class AnimalTypeModel(db.Model):
    __tablename__ = 'AnimalType'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, name: str, _id: int = None) -> None:
        self.id = _id
        self.name = name

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id, 'name': self.name}

    @classmethod
    def find_by_name(cls, name: str) -> AnimalTypeModel:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_attributes(cls, limit: int = None, offset: int = None) -> List:
        animalType = cls.query
        if limit:
            animalType = animalType.limit(limit)
        if offset:
            animalType = animalType.offset(offset)
        return animalType.all()

    @classmethod
    def find_by_id(cls, _id: int) -> AnimalTypeModel:
        return cls.query.filter_by(id=_id).first()

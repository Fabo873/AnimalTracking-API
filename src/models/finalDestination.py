from __future__ import annotations
from datetime import datetime

from helpers.db import db
from typing import List, Dict

from models.reception import ReceptionModel


class FinalDestinationModel(db.Model):
    __tablename__ = 'FinalDestinationData'

    id = db.Column(db.Integer, primary_key=True)
    specimen_id = db.Column(db.Integer, db.ForeignKey('SpecimenData.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('Destination.id'))
    condition = db.Column(db.String(100))
    weigth = db.Column(db.Integer)
    size = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    specimen = db.relationship('SpecimenModel')
    destination = db.relationship('DestinationModel')

    def __init__(self, specimen_id: int, destination_id: int, condition: str = None, weigth: int = None, size: int = None, notes: str = None,  _id: int = None) -> None:
        self.id = _id
        self.specimen_id = specimen_id
        self.destination_id = destination_id
        self.condition = condition
        self.weigth = weigth
        self.size = size
        self.notes = notes

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id,
                'date': str(self.created_at),
                'specimen': self.specimen.json(),
                'destination': self.destination.json(),
                'condition': self.condition,
                'weigth': self.weigth,
                'size': self.size,
                'notes': self.notes
                }

    @classmethod
    def find_by_specimen_id(cls, specimen_id: str) -> FinalDestinationModel:
        return cls.query.filter_by(specimen_id=specimen_id).first()

    @classmethod
    def find_by_attributes(cls, limit: int = None, offset: int = None, destination_id: int = None, specimen_id: int = None,
        person_id: int = None, animalType_id: int = None, species_id: int = None, gender_id: int = None, age_id: int = None, folio: str = None,
        date_from: datetime = None, date_to: datetime = None) -> List:

        finalDestination = cls.query
        if person_id or animalType_id or species_id or gender_id or age_id or folio:
            finalDestination = finalDestination.join(cls.specimen)
        if destination_id:
            finalDestination = finalDestination.filter_by(
                destination_id=destination_id)
        if specimen_id:
            finalDestination = finalDestination.filter_by(specimen_id=specimen_id)
        if person_id:
            finalDestination = finalDestination.filter_by(person_id=person_id)
        if animalType_id:
            finalDestination = finalDestination.filter_by(animalType_id=animalType_id)
        if species_id:
            finalDestination = finalDestination.filter_by(species_id=species_id)
        if gender_id:
            finalDestination = finalDestination.filter_by(gender_id=gender_id)
        if age_id:
            finalDestination = finalDestination.filter_by(age_id=age_id)
        if folio:
            finalDestination = finalDestination.filter_by(folio=folio)
        if date_from:
            finalDestination = finalDestination.filter(cls.created_at >= date_from)
        if date_to:
            finalDestination = finalDestination.filter(cls.created_at <= date_to)
        if limit:
            finalDestination = finalDestination.limit(limit)
        if offset:
            finalDestination = finalDestination.offset(offset)
        return finalDestination.all()

    @classmethod
    def find_by_id(cls, _id: int) -> FinalDestinationModel:
        return cls.query.filter_by(id=_id).first()

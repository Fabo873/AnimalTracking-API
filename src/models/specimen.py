from __future__ import annotations
from datetime import datetime

from helpers.db import db
from typing import List, Dict


class SpecimenModel(db.Model):
    __tablename__ = 'SpecimenData'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(100))
    person_id = db.Column(db.Integer, db.ForeignKey('Person.id'))
    animalType_id = db.Column(db.Integer, db.ForeignKey('AnimalType.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('Species.id'))
    gender_id = db.Column(db.Integer, db.ForeignKey('Gender.id'))
    age_id = db.Column(db.Integer, db.ForeignKey('Age.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('Destination.id'))
    condition = db.Column(db.String(200))
    weigth = db.Column(db.Float)
    size = db.Column(db.Float)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    person = db.relationship('PersonModel')
    animalType = db.relationship('AnimalTypeModel')
    species = db.relationship('SpeciesModel')
    gender = db.relationship('GenderModel')
    age = db.relationship('AgeModel')
    destination = db.relationship('DestinationModel')
    reception = db.relationship('ReceptionModel', back_populates="specimen")

    def __init__(self, folio: str, person_id: int, animalType_id: int, species_id: int, gender_id: int, age_id: int, destination_id: int, condition: str = None, weigth: float = None, size: float = None, _id: int = None) -> None:
        self.id = _id
        self.folio = folio
        self.person_id = person_id
        self.animalType_id = animalType_id
        self.species_id = species_id
        self.gender_id = gender_id
        self.age_id = age_id
        self.destination_id = destination_id
        self.condition = condition
        self.weigth = weigth
        self.size = size

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id,
                'folio': self.folio,
                'person': self.person.json(),
                'animalType': self.animalType.json(),
                'species': self.species.json(),
                'gender': self.gender.json(),
                'age': self.age.json(),
                'destination': self.destination.json(),
                'condition': self.condition,
                'weigth': self.weigth,
                'size': self.size}

    @classmethod
    def find_by_folio(cls, folio: str) -> SpecimenModel:
        return cls.query.filter_by(folio=folio).first()

    @classmethod
    def find_by_attributes(cls, limit: int = None, offset: int = None, person_id: int = None, animalType_id: int = None, species_id: int = None, gender_id: int = None, age_id: int = None, destination_id: int = None, folio: str = None,
        neighborhood_id: int = None, date_from: datetime = None, date_to: datetime = None) -> List:
        specimen = cls.query
        if neighborhood_id:
            specimen = specimen.join(cls.reception)
            specimen = specimen.filter_by(neighborhood_id=neighborhood_id)
        if person_id:
            specimen = specimen.filter_by(person_id=person_id)
        if animalType_id:
            specimen = specimen.filter_by(animalType_id=animalType_id)
        if species_id:
            specimen = specimen.filter_by(species_id=species_id)
        if gender_id:
            specimen = specimen.filter_by(gender_id=gender_id)
        if age_id:
            specimen = specimen.filter_by(age_id=age_id)
        if destination_id:
            specimen = specimen.filter_by(destination_id=destination_id)
        if folio:
            specimen = specimen.filter_by(folio=folio)
        if date_from:
            specimen = specimen.filter(cls.created_at >= date_from)
        if date_to:
            specimen = specimen.filter(cls.created_at <= date_to)
        if limit:
            specimen = specimen.limit(limit)
        if offset:
            specimen = specimen.offset(offset)
        return specimen.all()

    @classmethod
    def find_by_id(cls, _id: int) -> SpecimenModel:
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_specimen_day(cls, person_id: int) -> int:
        row = db.engine.execute(
            'SELECT COUNT(*) AS total FROM SpecimenData WHERE person_id = {} AND DATE(created_at) = CURDATE()'.format(str(person_id)))
        return row.first().total

from __future__ import annotations
from datetime import datetime

from helpers.db import db
from typing import List, Dict


class ReceptionModel(db.Model):
    __tablename__ = 'ReceptionData'

    id = db.Column(db.Integer, primary_key=True)
    deliver_person = db.Column(db.String(100))
    reciever_person_id = db.Column(db.Integer, db.ForeignKey('Person.id'))
    specimen_id = db.Column(db.Integer, db.ForeignKey('SpecimenData.id'))
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('Neighborhoods.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    reciever_person = db.relationship('PersonModel')
    specimen = db.relationship('SpecimenModel')
    neighborhood = db.relationship('NeighborhoodModel')

    def __init__(self, reciever_person_id: int, specimen_id: int, neighborhood_id: int = None, deliver_person: str = None, _id: int = None) -> None:
        self.id = _id
        self.deliver_person = deliver_person
        self.reciever_person_id = reciever_person_id
        self.specimen_id = specimen_id
        self.neighborhood_id = neighborhood_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> dict:
        return {'id': self.id,
                'date': str(self.created_at),
                'deliver_person': self.deliver_person,
                'reciever_person': self.reciever_person.json(),
                'specimen': self.specimen.json(),
                'neighborhood': self.neighborhood.json()
                }

    def csv(self) -> list:
        return [
            self.specimen.folio,
            self.deliver_person,
            self.reciever_person.name + ' ' + self.reciever_person.first_lastname + ' ' + self.reciever_person.second_lastname,
            self.neighborhood.name,
            self.neighborhood.municipality.name,
            self.neighborhood.municipality.state.name,
            str(self.created_at)
        ]

    @classmethod
    def getCsvLabels(cls) -> list:
       return [
            'Folio',
            'Persona que Entrega',
            'Persona que Recibe',
            'Colonia',
            'Municipio',
            'Estado',
            'Fecha'
        ] 

    @classmethod
    def find_by_specimen_id(cls, specimen_id: str) -> ReceptionModel:
        return cls.query.filter_by(specimen_id=specimen_id).first()

    @classmethod
    def find_by_attributes(cls, limit: int = None, offset: int = None, reciever_person_id: int = None, neighborhood_id: int = None, specimen_id: int = None,
        person_id: int = None, animalType_id: int = None, species_id: int = None, gender_id: int = None, age_id: int = None, folio: str = None,
        date_from: datetime = None, date_to: datetime = None) -> List:

        reception = cls.query
        if person_id or animalType_id or species_id or gender_id or age_id or folio:
            reception = reception.join(cls.specimen)
        if reciever_person_id:
            reception = reception.filter_by(
                reciever_person_id=reciever_person_id)
        if neighborhood_id:
            reception = reception.filter_by(neighborhood_id=neighborhood_id)
        if specimen_id:
            reception = reception.filter_by(specimen_id=specimen_id)
        if person_id:
            reception = reception.filter_by(person_id=person_id)
        if animalType_id:
            reception = reception.filter_by(animalType_id=animalType_id)
        if species_id:
            reception = reception.filter_by(species_id=species_id)
        if gender_id:
            reception = reception.filter_by(gender_id=gender_id)
        if age_id:
            reception = reception.filter_by(age_id=age_id)
        if folio:
            reception = reception.filter_by(folio=folio)
        if date_from:
            reception = reception.filter(cls.created_at >= date_from)
        if date_to:
            reception = reception.filter(cls.created_at <= date_to)
        if limit:
            reception = reception.limit(limit)
        if offset:
            reception = reception.offset(offset)
        return reception.all()

    @classmethod
    def find_by_id(cls, _id: int) -> ReceptionModel:
        return cls.query.filter_by(id=_id).first()

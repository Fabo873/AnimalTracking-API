from __future__ import annotations

from helpers.db import db
from typing import List, Dict


class ReceptionModel(db.Model):
    __tablename__ = 'ReceptionData'

    id = db.Column(db.Integer, primary_key=True)
    deliver_person = db.Column(db.String(100))
    reciever_person_id = db.Column(db.Integer, db.ForeignKey('Person.id'))
    specimen_id = db.Column(db.Integer, db.ForeignKey('SpecimenData.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('Locations.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    reciever_person = db.relationship('PersonModel')
    specimen = db.relationship('SpecimenModel')
    location = db.relationship('LocationModel')

    def __init__(self, reciever_person_id: int, specimen_id: int, location_id: int = None, deliver_person: str = None, _id: int = None) -> None:
        self.id = _id
        self.deliver_person = deliver_person
        self.reciever_person_id = reciever_person_id
        self.specimen_id = specimen_id
        self.location_id = location_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id,
                'deliver_person': self.deliver_person,
                'reciever_person': self.reciever_person.json(),
                'specimen': self.specimen.json(),
                'location': self.location.json()
                }

    @classmethod
    def find_by_specimen_id(cls, specimen_id: str) -> ReceptionModel:
        return cls.query.filter_by(specimen_id=specimen_id).first()

    @classmethod
    def find_by_attributes(cls, limit: int = None, offset: int = None, reciever_person_id: int = None, location_id: int = None, specimen_id: int = None) -> List:
        reception = cls.query
        if reciever_person_id:
            reception = reception.filter_by(
                reciever_person_id=reciever_person_id)
        if location_id:
            reception = reception.filter_by(location_id=location_id)
        if specimen_id:
            reception = reception.filter_by(specimen_id=specimen_id)
        if limit:
            reception = reception.limit(limit)
        if offset:
            reception = reception.offset(offset)
        return reception.all()

    @classmethod
    def find_by_id(cls, _id: int) -> ReceptionModel:
        return cls.query.filter_by(id=_id).first()

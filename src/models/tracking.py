from __future__ import annotations

from helpers.db import db
from typing import List, Dict
import datetime


class TrackingModel(db.Model):
    __tablename__ = 'TrackingData'

    id = db.Column(db.Integer, primary_key=True)
    specimen_id = db.Column(db.Integer, db.ForeignKey('SpecimenData.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('Destination.id'))
    condition = db.Column(db.String(100))
    weigth = db.Column(db.Integer)
    size = db.Column(db.Integer)
    reviewed = db.Column(db.Boolean)
    date = db.Column(db.Date())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    specimen = db.relationship('SpecimenModel')
    destination = db.relationship('DestinationModel')

    def __init__(self, specimen_id: int, destination_id: int, date: datetime.date, condition: str = None, weigth: int = None, size: int = None, reviewed: bool = False,  _id: int = None) -> None:
        self.id = _id
        self.specimen_id = specimen_id
        self.destination_id = destination_id
        self.date = date
        self.condition = condition
        self.weigth = weigth
        self.size = size
        self.reviewed = reviewed

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id,
                'date': str(self.date),
                'specimen': self.specimen.json(),
                'destination': self.destination.json(),
                'condition': self.condition,
                'weigth': self.weigth,
                'size': self.size,
                'reviewed': self.reviewed
                }

    @classmethod
    def find_by_specimen_id(cls, specimen_id: str) -> TrackingModel:
        return cls.query.filter_by(specimen_id=specimen_id).first()

    @classmethod
    def find_by_attributes(cls, limit: int = None, offset: int = None, destination_id: int = None, specimen_id: int = None, reviewed: bool = None) -> List:
        tracking = cls.query
        if destination_id:
            tracking = tracking.filter_by(destination_id=destination_id)
        if specimen_id:
            tracking = tracking.filter_by(specimen_id=specimen_id)
        if reviewed:
            tracking = tracking.filter_by(reviewed=reviewed)
        if limit:
            tracking = tracking.limit(limit)
        if offset:
            tracking = tracking.offset(offset)
        return tracking.all()

    @classmethod
    def find_by_id(cls, _id: int) -> TrackingModel:
        return cls.query.filter_by(id=_id).first()

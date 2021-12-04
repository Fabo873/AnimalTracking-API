from __future__ import annotations
from helpers.db import db
from typing import List, Dict


class MunicipalityModel(db.Model):
    __tablename__ = 'Municipalities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    state_id = db.Column(db.Integer, db.ForeignKey('States.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    state = db.relationship('StateModel', back_populates="municipalities")
    neighborhoods = db.relationship(
        'NeighborhoodModel', lazy='dynamic', back_populates="municipality")

    def __init__(self, name: str, state_id: int, _id: int = None) -> None:
        self.id = _id
        self.name = name
        self.state_id = state_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id, 'name': self.name, 'state': self.state.json()}

    @classmethod
    def find_by_attributes(cls, name: str = None, state_id: int = None, limit: int = None, offset: int = None) -> List:
        municipalities = cls.query
        if name:
            search = "%{}%".format(name)
            municipalities = municipalities.filter(cls.name.like(search))
        if state_id:
            municipalities = municipalities.filter_by(state_id=state_id)
        if limit:
            municipalities = municipalities.limit(limit)
        if offset:
            municipalities = municipalities.offset(offset)
        return municipalities.all()

    @classmethod
    def find_by_id(cls, _id: int) -> MunicipalityModel:
        return cls.query.filter_by(id=_id).first()

from __future__ import annotations
from helpers.db import db
from typing import List, Dict


class StateModel(db.Model):
    __tablename__ = 'States'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    initials = db.Column(db.String(50))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    municipalities = db.relationship(
        'MunicipalityModel', lazy='dynamic', back_populates="state")

    def __init__(self, name: str, initials: str, _id: int = None) -> None:
        self.id = _id
        self.name = name
        self.initials = initials

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id, 'name': self.name, 'initials': self.initials}

    @classmethod
    def find_by_name(cls, name: str) -> StateModel:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_attributes(cls, name: str = None, limit: int = None, offset: int = None) -> List:
        states = cls.query
        if name:
            search = "%{}%".format(name)
            states = states.filter(cls.name.like(search))
        if limit:
            states = states.limit(limit)
        if offset:
            states = states.offset(offset)
        return states.all()

    @classmethod
    def find_by_id(cls, _id: int) -> StateModel:
        return cls.query.filter_by(id=_id).first()

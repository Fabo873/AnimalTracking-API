from __future__ import annotations
from helpers.db import db
from typing import List, Dict


class AgeModel(db.Model):
    __tablename__ = 'Age'

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

    def json(self) -> dict:
        return {'id': self.id, 'name': self.name, 'created_at': str(self.created_at.day), 'type': str(type(self.created_at))}

    @classmethod
    def find_by_name(cls, name: str) -> AgeModel:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_attributes(cls, name: str = None, limit: int = None, offset: int = None) -> list:
        age = cls.query
        if name:
            search = "%{}%".format(name)
            age = age.filter(cls.name.like(search))
        if limit:
            age = age.limit(limit)
        if offset:
            age = age.offset(offset)
        return age.all()

    @classmethod
    def find_by_id(cls, _id: int) -> AgeModel:
        return cls.query.filter_by(id=_id).first()

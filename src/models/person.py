from __future__ import annotations
from helpers.db import db
from typing import List, Dict


class PersonModel(db.Model):
    __tablename__ = 'Person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    first_lastname = db.Column(db.String(50))
    second_lastname = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    user = db.relationship(
        'UserModel', back_populates="person")

    def __init__(self, name: str, first_lastname: str, second_lastname: str, user_id: int, _id: int = None) -> None:
        self.id = _id
        self.name = name
        self.first_lastname = first_lastname
        self.second_lastname = second_lastname
        self.user_id = user_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> Dict:
        return {'id': self.id, 'name': self.name, 'first_lastname': self.first_lastname, 'second_lastname': self.second_lastname, 'user_id': self.user_id}

    @classmethod
    def find_by_name(cls, name: str, first_lastname: str, second_lastname: str) -> PersonModel:
        return cls.query.filter_by(name=name, first_lastname=first_lastname, second_lastname=second_lastname).first()

    @classmethod
    def find_by_attributes(cls, name: str = None, limit: int = None, offset: int = None) -> List:
        persons = cls.query
        if name:
            search = "%{}%".format(name)
            persons = persons.filter((cls.name.like(search)) | (
                cls.first_lastname.like(search)) | (cls.second_lastname.like(search)))
        if limit:
            persons = persons.limit(limit)
        if offset:
            persons = persons.offset(offset)
        return persons.all()

    @classmethod
    def find_by_id(cls, _id: int) -> PersonModel:
        return cls.query.filter_by(id=_id).first()

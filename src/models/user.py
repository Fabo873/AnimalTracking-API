from __future__ import annotations
from helpers.db import db
from typing import List, Dict
from helpers.encryption import Encryption


class UserModel(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(500))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    person = db.relationship(
        'PersonModel', lazy='dynamic', back_populates="user")

    def __init__(self, username: str, password: str, _id: int = None) -> None:
        self.id = _id
        self.username = username
        self.password = Encryption.encode(password)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> dict:
        return {'id': self.id, 'username': self.username, 'password': self.password, 'descrypted': Encryption.decode(self.password)}

    @classmethod
    def find_by_username(cls, username: str) -> UserModel:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_attributes(cls, limit: int = None, offset: int = None) -> list:
        users = cls.query
        if limit:
            users = users.limit(limit)
        if offset:
            users = users.offset(offset)
        return users.all()

    @classmethod
    def find_by_id(cls, _id: int) -> UserModel:
        return cls.query.filter_by(id=_id).first()

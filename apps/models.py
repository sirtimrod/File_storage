from typing import Type
from typing_extensions import Self

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

user_file = db.Table('user_file',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('file_id', db.Integer, db.ForeignKey('files.id'))
)

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String,
        unique=False,
        nullable=False
    )
    password = db.Column(
        db.String,
        unique=False,
        nullable=False
    )
    files = db.relationship('File', secondary='user_file', backref='users')

    @classmethod
    def get_user(cls, username: str, password: str) -> Self:
        user = cls.query.filter_by(
            username=username, 
            password=password).first()
        return user
    
    @classmethod
    def add_user(cls, **kwargs: str):
        user = cls(**kwargs)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def append_file(cls, file: Type[Self], username: str, password: str):
        user = cls.get_user(username, password)
        user.files.append(file)
        db.session.commit()
    
    @classmethod
    def delete_appended_file(cls, file: Type[Self], username: str, password: str):
        user = cls.get_user(username, password)
        user.files.remove(file)
        db.session.commit()

    @classmethod
    def check_file(cls, file: Type[Self], username: str, password: str) -> bool:
        user = cls.get_user(username, password)
        return file in user.files


class File(db.Model):

    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(
        db.String,
        unique=False,
        nullable=True
    )
    extension = db.Column(
        db.String,
        unique=False,
        nullable=True
    )
    hash = db.Column(
        db.String,
        unique=True,
        nullable=False
    )

    @classmethod
    def get_file(cls, hash: str) -> Self:
        file = cls.query.filter_by(hash=hash).first()
        return file
    
    @classmethod
    def add_file(cls, **kwargs: str) -> Self:
        file = cls(**kwargs)
        db.session.add(file)
        db.session.commit()
        return file

    @classmethod
    def delete_file(cls, hash: str):
        file = cls.get_file(hash)
        db.session.delete(file)
        db.session.commit()

    @classmethod
    def check_users(cls, hash: str) -> int:
        file = cls.get_file(hash)
        return len(file.users)

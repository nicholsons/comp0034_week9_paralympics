from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from paralympics_app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profile = db.relationship('Profile', back_populates='user')

    def __init__(self, first_name: str, last_name: str, email: str, password_text: str):
        """
        Create a new User object using hashing the plain text password.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self._generate_password_hash(password_text)

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password}"

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def set_password(self, password: str):
        self.password = self._generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    photo = db.Column(db.Text)
    bio = db.Column(db.Text)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='profile')


class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.Text)


class Medals(db.Model):
    __tablename__ = 'medals'
    id = db.Column(db.Integer, primary_key=True)
    Rank = db.Column(db.Text)
    Country = db.Column(db.Text)
    NPC = db.Column(db.Text)
    Gold = db.Column(db.Text)
    Silver = db.Column(db.Text)
    Bronze = db.Column(db.Text)
    Total = db.Column(db.Text)
    Event = db.Column(db.Text)
    Year = db.Column(db.Text)


class CompetitionEntry(db.Model):
    __tablename__ = 'competition_entry'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Text, nullable=False)
    q2 = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

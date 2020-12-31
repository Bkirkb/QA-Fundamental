from application import db
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base



class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(35), nullable=False, unique=True)
    minweight = db.Column(db.Integer, nullable=False)
    maxweight = db.Column(db.Integer, nullable=False)
    catches = db.relationship('Catches', backref="catches", lazy=True)

class Catches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fishname = db.Column(db.String(35), nullable=False)
    fishid = db.Column(db.Integer, db.ForeignKey('fish.id'), nullable=False)
    fishweight = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=True)

from application import db
from datetime import datetime




class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    forename = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    gear = db.Column(db.String(255), nullable=True)
    catches = db.relationship('Catchdiary', backref='totalcatches')
    topcatches = db.relationship('Catchdiary', backref='totaltopcatches')


class Fish(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fishname = db.Column(db.String(50), nullable=False)
    minweight = db.Column(db.Numeric, nullable=False)
    maxweight = db.Column(db.Numeric, nullable=False)
    avgweight = db.Column(db.Numeric, nullable=False)

class Catchdiary(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fishid = db.Column(db.Integer, db.ForeignKey('fish.id'), nullable=False)
    fishweight = db.Column(db.Numeric, nullable=False)
    timetk = db.Column(db.DateTime, nullable=False)
    dateoc = db.Column(db.DateTime, nullable=False)
    weather = db.Column(db.String(20), nullable=True)
    catchdesc = db.Column(db.String(100), nullable=True)
    topcatch = db.Column(db.Boolean, nullable=False)
    totalcatches = db.Column(db.Integer, nullable=False)
    totaltopcatches = db.Column(db.Integer, nullable=False)

class Mostactive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))
    catches = db.Column(db.Integer, db.ForeignKey('Catchdiary.totalcatches', nullable=False))
    topcatches = db.Column(db.Integer, db.ForeignKey('Catchdiary.totaltopcatches', nullable=False))
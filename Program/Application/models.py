from application import db
from datetime import datetime



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(15), nullable=False)
    forename = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gear = db.Column(db.String(255), nullable=True)
    catches = db.Column(db.Integer, foreign_key=True, backref=Catchdiary.catches)
    topcatches = db.Column(db.Integer, foreign_key=True, backref=Catchdiary.topcatches)


class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fishname = db.Column(db.String(50), nullable=False)
    minweight = db.Column(db.Decimal, nullable=False)
    maxweight = db.Column(db.Decimal, nullable=False)
    avgweight = db.Column(db.Decimal, nullable=False)

class Catchdiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, foreign_key=True, backref=Users.id)
    fishid = db.Column(db.Integer, foreign_key=True, backref=Fish.id)
    fishweight = db.Column(db.Decimal, nullable=False)
    timetk = db.Column(db.DateTime, nullable=False)
    dateoc = db.Column(db.DateTime, nullable=False)
    weather = db.Column(db.String(20), nullable=True)
    catchdesc = db.Column(db.String(100), nullable=True)
    topcatch = db.Column(db.Boolean, nullable=False)
    totalcatches = db.Column(db.Integer, nullable=False)
    totaltopcatches = db.Column(db.Integer, nullable=False)

class Mostactive(db.Model):
    userid = db.Column(db.Integer, primary_key=True, backref=Users.id)
    catches = db.Column(db.Integer, foreign_key=True, backref=Catchdiary.totalcatches)
    topcatches = db.Column(db.Integer, foreign_key=True, backref=Catchdiary.totaltopcatches)
from application import app, db
from application.models import Catches, Fish
from flask import Flask, render_template, request, redirect, url_for
from application.forms import  CatchForm

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    all_catches = Catches.query.all()
    all_fish = Fish.query.all()
    output = ""
    return render_template('home.html', title="Home", all_catches=all_catches, all_fish=all_fish)

@app.route('/create', methods = ["GET", "POST"])
def create():
    form = CatchForm()
    all_fish = Fish.query.all()

    if request.method == "POST":
        all_fish = Fish.query.all()
        if form.validate_on_submit():
            # can't run for statement with an empty array, this stops the app from returning null values when the database population has been reset.
            if all_fish == []:
                new_fish = Fish(name=form.name.data.lower(), minweight=form.weight.data, maxweight=form.weight.data)
                db.session.add(new_fish)
                db.session.commit()
                new_catch = Catches(fishid=new_fish.id, fishname=form.name.data.lower(), fishweight=form.weight.data, description=form.description.data.lower())
                db.session.add(new_catch)
                db.session.commit()
                return redirect(url_for("home"))
            else:
                fishlen = len(all_fish)
                # for each fish in the fish dictionary check if entered fish is part of the records.
                for fish in all_fish:
                    if form.name.data.lower() == fish.name:
                        new_catch = Catches(fishid=fish.id, fishname=fish.name.lower(), fishweight=form.weight.data, description=form.description.data.lower())
                        db.session.add(new_catch)
                        # Change fish min and max values if new catch eclipses old value
                        if new_catch.fishweight < fish.minweight:
                            fish.minweight = new_catch.fishweight
                            db.session.commit()
                        elif new_catch.fishweight > fish.maxweight:
                            fish.maxweight = new_catch.fishweight
                            db.session.commit()
                        db.session.commit()
                        return  redirect(url_for("home"))
                # outside of for statement to avoid duplicate errors
                new_fish = Fish(name=form.name.data.lower(), minweight=form.weight.data, maxweight=form.weight.data)
                db.session.add(new_fish)
                db.session.commit()
                new_catch = Catches(fishid=new_fish.id, fishname=form.name.data.lower(), fishweight=form.weight.data, description=form.description.data.lower())
                db.session.add(new_catch)
                db.session.commit()     
            return redirect(url_for("home"))
    return render_template('add.html', title="Create a Task", form=form)

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    form = CatchForm()
    catch = Catches.query.filter_by(id=id).first()
    if request.method == "POST":
        catch.description = form.description.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update.html", form=form, title="Update Catch Description",catch=catch)

@app.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    catch = Catches.query.filter_by(id=id).first()
    db.session.delete(catch)
    db.session.commit()
    return redirect(url_for("home"))

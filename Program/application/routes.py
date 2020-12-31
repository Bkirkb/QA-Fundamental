from application import app, db
from application.models import Catchdiary, Fish, Users
from flask import Flask, render_template, request, redirect, url_for
from application.forms import LogForm

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
   # all_catches = Catchdiary.query.all()
    form = LogForm()
    if request.method == "POST":
        if form.validate_on_submit():
            exists = db.session.query(
            db.session.query(User).filter_by(name=form.username.data).exists()
            ).scalar()
            if exists == True:
                return redirect(url_for("home"))
            elif exists == False:
                new_user = Users(username=form.username.data, userpassword=form.userpassword.data, forename=form.forename.data, surname=form.surname.data, email=form.email.data, gear=form.gear.data)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("home"))
    return render_template('home.html', title="Home", form=form)

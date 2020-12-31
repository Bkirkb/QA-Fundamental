from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired


class CatchForm(FlaskForm):
    name = StringField('Name of Fish', validators=[DataRequired()])
    weight = IntegerField('Weight of Fish (lbs)', validators=[DataRequired()])
    description = StringField('Describe the catch!')
    submit = SubmitField ('Add Fish')
    submit2 = SubmitField('Change Description')
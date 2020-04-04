from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CelestialDataForm(FlaskForm):
    object = StringField('Object', validators=[DataRequired(), Length(min=2, max=20)])
    radius = StringField('Radius (m)', validators=[DataRequired(), ])
    mass = StringField('Mass (kg)', validators=[DataRequired()])
    submit = SubmitField('Submit Data')

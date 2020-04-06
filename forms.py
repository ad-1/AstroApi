from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CelestialDataForm(FlaskForm):
    body = TextAreaField('JSON Data', validators=[DataRequired()])
    submit = SubmitField('Submit Data')

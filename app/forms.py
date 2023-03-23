from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, EqualTo


class AddInfo(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    number = StringField('Number', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    submit = SubmitField('Add Information')

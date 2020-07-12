from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class UpdUserForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Update User')
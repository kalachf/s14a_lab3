from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class DelUserForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Delete User')
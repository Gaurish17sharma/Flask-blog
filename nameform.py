from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    username = StringField('What is Your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
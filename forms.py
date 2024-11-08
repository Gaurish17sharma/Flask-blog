from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField , ValidationError, validators
from wtforms.validators import DataRequired , EqualTo  , Length

class NameForm(FlaskForm):
    username = StringField('What is Your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    fav_color = StringField('Favourite Color')
    password_hash = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('password_hash2',
                            message='Passwords must match')])
    password_hash2 = PasswordField('Confirm Password',[validators.DataRequired()] )
    submit = SubmitField('Submit')
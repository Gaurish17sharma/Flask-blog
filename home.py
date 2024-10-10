from flask import Flask , render_template , flash
from nameform import NameForm , UserForm
from config import Config
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime , timezone


# flask instance
app = Flask(__name__)
# secret key
app.config['SECRET_KEY'] = Config.SECRET_KEY
# adding database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# initialize the database
db = SQLAlchemy(app)

app.app_context().push()

# creating a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return { 'id': self.id , 'username': self.username, 'email': self.email }
    
db.create_all()

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    username = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(username = form.username.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ' '
        form.email.data = ' '
        flash("User Added Successfully!!!")

    return render_template('add_user.html' ,
                           form = form, 
                           username = username)

@app.route('/')

def index():
    users = {'username': 'Gaurish Sharma'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html' , title ='Home' , 
                           users = users, 
                           posts = posts)

@app.route('/user/<name>')

def user(name):
    return render_template('user.html', 
                           name = name )


@app.route('/name' , methods=['GET', 'POST'])
def name():
    username = None
    form = NameForm()
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ' '
        flash("Form Submitted Successfully!!!")

    return render_template('name.html', 
                           username = username , 
                           form=form)




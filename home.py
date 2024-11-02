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
# adding old database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# adding new database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gaurishsharma:password@localhost/flask_users'
# initialize the database
db = SQLAlchemy(app)

app.app_context().push()

# creating a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_added = db.Column(db.DateTime , default = datetime.now(timezone.utc))

    def __repr__(self):
        return { 'id': self.id , 'username': self.username, 'email': self.email, 'date added': self.date_added }
    
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
    
    my_users = Users.query.order_by(Users.id)
    return render_template('add_user.html' ,
                           form = form, 
                           username = username,
                           my_users = my_users)


# updating database
@app.route('/update/<int:id>', methods = ['GET' , 'POST'])
def update_list(id):
    form = UserForm()
    updating_users = Users.query.get_or_404(id)
    if form.validate_on_submit():
        updating_users = Users(username = form.username.data , email = form.email.data)
        try:
            db.session.commit()
            flash('User Updataed Successfully!!!')
            return render_template('update.html',
                                   form = form,
                                   updating_users = updating_users)
        except:
            flash('Error... please Try Again')
            return render_template('update.html',
                                   form = form,
                                   updating_users = updating_users)
    else:
        return render_template('update.html',
                                   form = form,
                                   updating_users = updating_users)





@app.route('/user/list' , methods =['GET', 'POST'])
def user_list():   
    my_users = Users.query.order_by(Users.id)
    return render_template('user_list.html' ,
                           my_users = my_users)



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

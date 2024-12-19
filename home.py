from flask import Flask , render_template , flash , redirect , url_for
from forms import NameForm , UserForm , UserUpdationForm , Postform , Loginform
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ
from datetime import datetime , timezone , date
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user , current_user 

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
migrate = Migrate(app , db)

#flask-login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#creating login page
@app.route('/login', methods =['GET','POST'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password_hash , form.password_hash.data):
                login_user(user)
                flash('Login Successful!!!')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password - Try Again...')
        else:
            flash('This User Does not Exist')
    return render_template('login.html' , 
                       form = form)

@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    flash('You have been Logged Out')
    return redirect(url_for('login'))


#creating User Dashboard page
@app.route('/dashboard', methods =['GET','POST'])
@login_required
def dashboard():  
    return render_template('dashboard.html')

#creating blog model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime , default = datetime.now(timezone.utc))
    slug = db.Column(db.String(255))

#adding posts
@app.route('/add_post', methods=['GET','POST'])
@login_required
def add_post():
    title = None
    form = Postform()
    if form.validate_on_submit():
        post = Posts(title = form.title.data ,
                     content = form.content.data,
                     author = form.author.data,
                     slug = form.slug.data)
        
        db.session.add(post)
        db.session.commit()
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data =''

        flash("Post Added Successfully!!!")

    return render_template('add_post.html',
                           form = form)

#indvidual post
@app.route('/posts/<int:id>' , methods =['GET','POST'])
def view_post(id):
    post = Posts.query.get_or_404(id)
    return render_template('view_post.html',
                           post = post)

#update post
@app.route('/update_post/<int:id>' , methods = ['GET','POST'])
@login_required
def update_post(id):
    form = Postform()
    updating_post = Posts.query.get_or_404(id)
    if form.validate_on_submit():
        updating_post.title = form.title.data
        updating_post.author = form.author.data
        updating_post.slug = form.slug.data
        updating_post.content = form.content.data
        try:
            print("does validate...")
            db.session.commit()
            flash('Post Updated Successfully!!!')
            return redirect(url_for('view_post', id = id))
        except:
            flash('Error... please Try Again')
            return render_template('update_post.html',
                                   form = form,
                                   updating_post = updating_post
                                   )
    form.title.data = updating_post.title
    form.author.data = updating_post.author
    form.slug.data = updating_post.slug
    form.content.data = updating_post.content
    return render_template('update_post.html',
                                form = form)

#deleting a post
@app.route('/delete_post/<int:id>' , methods = ['GET','POST'])
@login_required
def delete_post(id):
    deleting_post = Posts.query.get_or_404(id)
    try:
        db.session.delete(deleting_post)
        db.session.commit()
        flash("Post Deleted Successfully!!")

        my_posts = Posts.query.order_by(Posts.date_posted)
        return render_template('blog_posts.html' ,
                           my_posts = my_posts)
    
    except:
        flash("There was an error in deleing the user try again!!")
        my_posts = Posts.query.order_by(Posts.date_posted)
        return render_template('blog_posts.html' ,
                           my_posts = my_posts)

#posts list
@app.route('/post/list' , methods =['GET', 'POST'])
def blog_post():
    my_posts = Posts.query.order_by(Posts.date_posted)
    return render_template('blog_posts.html' ,
                           my_posts = my_posts)


# creating a User model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False , unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_added = db.Column(db.DateTime , default = datetime.now(timezone.utc))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash , password)
    
    def __repr__(self):
        return '<Users %r>' % self.username

#adding user
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    username = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_password = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
            user = Users(username = form.username.data, 
                         email = form.email.data, 
                         password_hash = hashed_password)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ' '
        form.email.data = ' '
        flash("User Added Successfully!!!")
    
    my_users = Users.query.order_by(Users.id)
    return render_template('signup.html' ,
                           form = form, 
                           username = username,
                           my_users = my_users)


# updating user info
@app.route('/update_list/<int:id>', methods = ['GET' , 'POST'])
def update_list(id):
    print(id)
    form = UserUpdationForm()
    updating_users = Users.query.get_or_404(id)
    if form.validate_on_submit():
        updating_users.username =  form.username.data 
        updating_users.email = form.email.data
        try:
            print("does validate...")
            db.session.commit()
            flash('User Updated Successfully!!!')
            return render_template('update_list.html',
                                   form = form,
                                   updating_users = updating_users,
                                   id = id
                                   )
        except:
            flash('Error... please Try Again')
            return render_template('update_list.html',
                                   form = form,
                                   updating_users = updating_users
                                   )
    else:
        return render_template('update_list.html',
                                   form = form,
                                   updating_users = updating_users,
                                   id = id)

#deleting user
@app.route('/delete_user/<int:id>', methods = ['GET' , 'POST'])
def delete_user(id):
    form = UserForm()
    username = None
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")

        my_users = Users.query.order_by(Users.id)
        return render_template('add_user.html' ,
                           form = form, 
                           username = username,
                           my_users = my_users)
        
    except:
        flash("There was an error in deleing the user try again!!")
        my_users = Users.query.order_by(Users.id)
        return render_template('add_user.html' ,
                           form = form, 
                           username = username,
                           my_users = my_users)


#user list
@app.route('/user/list' , methods =['GET', 'POST'])
def user_list():
    my_users = Users.query.order_by(Users.id)
    return render_template('user_list.html' ,
                           my_users = my_users)



#example
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

#practice route
@app.route('/user/<name>')

def user(name):
    return render_template('user.html', 
                           name = name )


#nameform
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

#date json
@app.route('/date')
def current_date():
    return { "Date": date.today() }
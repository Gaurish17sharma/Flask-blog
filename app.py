from flask import Flask , render_template , flash , redirect , url_for
from forms import NameForm , UserForm , UserUpdationForm , Postform , Loginform
from config import Config
from flask_migrate import Migrate
from datetime import datetime , timezone , date
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user , current_user
from models import Posts , Users , db
from controllers.login_route import loginform
from controllers.post_route import add_postform , update_postform , delete_postform
from controllers.user_route import add_userform , update_listform , delete_userform

# flask instance
app = Flask(__name__)
# secret key
app.config['SECRET_KEY'] = Config.SECRET_KEY
# adding old database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# adding new database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gaurishsharma:password@localhost/flask_users'
# initialize the database

app.app_context().push()
db.init_app(app)
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
    loginform()
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


#adding posts
@app.route('/add_post', methods=['GET','POST'])
@login_required
def add_post():
    title = None
    form = Postform()
    add_postform()
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
    update_postform(id)
    form.title.data = updating_post.title
    form.slug.data = updating_post.slug
    form.content.data = updating_post.content
    return render_template('update_post.html',
                                form = form)

#deleting a post
@app.route('/delete_post/<int:id>' , methods = ['GET','POST'])
@login_required
def delete_post(id):
    delete_postform(id)
    my_posts = Posts.query.order_by(Posts.date_posted)
    return render_template('blog_posts.html',
                           my_posts = my_posts)
    

#posts list
@app.route('/post/list' , methods =['GET', 'POST'])
def blog_post():
    my_posts = Posts.query.order_by(Posts.date_posted)
    return render_template('blog_posts.html' ,
                           my_posts = my_posts) 


#adding user
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    form = UserForm()
    add_userform()
    my_users = Users.query.order_by(Users.id)
    return render_template('signup.html' ,
                           form = form,
                           my_users = my_users)


# updating user info
@app.route('/update_list/<int:id>', methods = ['GET' , 'POST'])
def update_list(id):
    form = UserUpdationForm()
    update_listform(id)
    updating_users = Users.query.get_or_404(id)
    return render_template('update_list.html',
                                   form = form,
                                   updating_users = updating_users,
                                   id = id)


#deleting user
@app.route('/delete_user/<int:id>', methods = ['GET' , 'POST'])
def delete_user(id):
    form = UserForm()
    delete_userform(id)
    my_users = Users.query.order_by(Users.id)
    return render_template('signup.html' ,
                           form = form, 
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
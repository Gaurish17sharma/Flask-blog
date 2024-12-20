from app import app
from forms import NameForm , UserForm , UserUpdationForm , Postform , Loginform
from models import Posts , Users , db
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Flask , render_template , flash , redirect , url_for
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user , current_user

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
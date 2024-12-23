from models import Users , db
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Flask , render_template , flash , redirect , url_for
from forms import Loginform
from flask_login import login_user , login_required , logout_user , current_user

#for login form
def loginform():
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
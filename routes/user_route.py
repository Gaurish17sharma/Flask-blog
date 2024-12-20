from app import app
from forms import NameForm , UserForm , UserUpdationForm , Postform , Loginform
from models import Posts , Users , db
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Flask , render_template , flash , redirect , url_for


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
        flash("Account Created Successfully!!!")
        return redirect(url_for('login')) 
    
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
            flash('Profile Updated Successfully!!!')
            return redirect(url_for('dashboard'))
                                   
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
        return render_template('signup.html' ,
                           form = form, 
                           username = username,
                           my_users = my_users)
        
    except:
        flash("There was an error in deleing the user try again!!")
        my_users = Users.query.order_by(Users.id)
        return render_template('signup.html' ,
                           form = form, 
                           username = username,
                           my_users = my_users)

#user list
@app.route('/user/list' , methods =['GET', 'POST'])
def user_list():
    my_users = Users.query.order_by(Users.id)
    return render_template('user_list.html' ,
                           my_users = my_users)
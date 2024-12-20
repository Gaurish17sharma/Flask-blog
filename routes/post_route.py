from app import app
from forms import NameForm , UserForm , UserUpdationForm , Postform , Loginform
from models import Posts , Users , db
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Flask , render_template , flash , redirect , url_for
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user , current_user

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
from flask import Flask , render_template
from nameform import NameForm
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

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
    return render_template('index.html' , title ='Home' , users = users, posts = posts)

@app.route('/user/<name>')

def user(name):
    return render_template('user.html', name = name )


@app.route('/name' , methods=['GET', 'POST'])
def name():
    username = None
    form = NameForm()
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = None
    return render_template('name.html', username = username , form=form)



import os

from flask import Flask, render_template, url_for, redirect, flash
from time import localtime, strftime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

# socket io
from flask_socketio import SocketIO, send, emit, join_room, leave_room


# import model of db from models.py
from models import *

#import everything from wtform_fields
from wtform_fields import *

# Configure App
#wsgei there has to be central callable obj
app = Flask(__name__)

# Configure db
# We need to tell flask the location of db we will access and mod
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

# create secret key to keep client session secure, cookies during sess
app.secret_key = os.environ.get("SECRET")

# Instantiate Flask-socket io and pass in app.
socketio = SocketIO(app)

# initialize list of rooms
ROOMS = ["lounge", "news", "games", "coding"]

#  user loader function
@login.user_loader
def load_user(id):

    return User.query.get(int(id))

# decorator is activate symbol
@app.route('/', methods=['GET', 'POST'])
def index():
    
    # instantiate registration form
    reg_form = RegistrationForm()

    # shortcut to trigger validators
    # reg_form is name of form
    # will return true if form submit w post and cleared conditions
    # else return false
    reg_form.validate_on_submit()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Auto hashed and $alted!
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        # Flask built in message flashing system
        flash('Registered successfully. Please login.', 'success')

        return redirect(url_for('login'))


    # when installing flask, it installs Jinja
    # reusable templates for web app.
    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # if success, login
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        # current user is proxy for user_object, is_authenticated came with
        # UserMixin
        return redirect(url_for('chat'))
        
    
    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('Logged out successfully', "success")
    return redirect(url_for('login'))


# event bucket/handeler for socket io
@socketio.on('message')
def message(data):

    # if client sends data, simply print message to terminal
    print(f"\n\n{data}\n\n")

    # broadcast message to all connected clients
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': 
        strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])
    # %b gives us abbr month -%d day of month %I hours, %m minutes %p am or pm and applied to localtime    

    # both client and server can only recieve messages in particular buckets

@socketio.on('join')
def join(data):

    join_room(data['room'])

    send({'msg': data['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])

    send({'msg': data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])

# when run from terminal python will always validate this condition
# to be true
# updated for socketio
if __name__ == '__main__':
    app.run()
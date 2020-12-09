from flask import Flask, render_template, url_for, redirect, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

# import model of db from models.py
from models import *

#import everything from wtform_fields
from wtform_fields import *

# Configure App
#wsgei there has to be central callable obj
app = Flask(__name__)

# Configure db
# We need to tell flask the location of db we will access and mod
app.config['SQLALCHEMY_DATABASE_URI']='postgres://tqhtmhdvlrvncj:409dab96337fd78dea74bf6d1367818c04f803b89e5f614a2e89c729b9ad83e5@ec2-34-192-122-0.compute-1.amazonaws.com:5432/d8gh9apsp8ul1n'
db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

# create secret key to keep client session secure, cookies during sess
app.secret_key = 'replace'

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

    return "Chat here."

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('Logged out successfully', "success")
    return redirect(url_for('login'))


# when run from terminal python will always validate this condition
# to be true
if __name__ == '__main__':
    app.run(debug=True)
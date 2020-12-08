from flask import Flask, render_template

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

# create secret key to keep client session secure, cookies during sess
app.secret_key = 'replace'

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

        #  check if username exists
        user_object = User.query.filter_by(username=username).first()
        
        if user_object:
            return "Username taken"
        
        # Add user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted to DB"


    # when installing flask, it installs Jinja
    # reusable templates for web app.
    return render_template("index.html", form=reg_form)

# when run from terminal python will always validate this condition
# to be true
if __name__ == '__main__':
    app.run(debug=True)
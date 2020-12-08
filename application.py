from flask import Flask, render_template

#import everything from wtform_fields
from wtform_fields import *

# Configure App
#wsgei there has to be central callable obj
app = Flask(__name__)

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
        return "Success!"
  

    # when installing flask, it installs Jinja
    # reusable templates for web app.
    return render_template("index.html", form=reg_form)

# when run from terminal python will always validate this condition
# to be true
if __name__ == '__main__':
    app.run(debug=True)
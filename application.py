from flask import Flask, render_template

#wsgei there has to be central callable obj
app = Flask(__name__)

# create secret key to keep client session secure, cookies during sess
app.secret_key = 'replace'

# decorator is activate symbol
@app.route('/', methods=['GET', 'POST'])
def index():
    
    # when installing flask, it installs Jinja
    # reusable templates for web app.
    return render_template("index.html")

# when run from terminal python will always validate this condition
# to be true
if __name__ == '__main__':
    app.run(debug=True)
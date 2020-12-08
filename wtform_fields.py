from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from models import User

# input required: cant leave blank, what length for field, if not identical error
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    """ Registration form """
    # username, password, passconfirm
    # each will be a class attribute

    # this will be used only when field is rendered in html file <label>
    username = StringField('username_label', 
        validators=[InputRequired(message="Username required"),
        Length(min=4, max=25, message="""Username must be between 4 and
        25 characters""")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=25, message="""Password must be between 4 and
        25 characters""")])
    confirm_pswd = PasswordField('confirm_pswd_label',
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        #  check if duplicate
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select another.")


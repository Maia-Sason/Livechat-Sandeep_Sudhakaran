from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# UserMixin tells flask login about our user
class User(UserMixin, db.Model):
    """ User Model """
    #  without giving a name, class sqlalchemy will
    #  take name of class as table

    #  To access table:
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)



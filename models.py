"""Models for Auth"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Table"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow,
                             onupdate=datetime.utcnow)

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<User {u.username} {u.first_name} {u.last_name} {u.created_date} {u.updated_date}>"

    @classmethod
    def full_name(cls, username):
        """ Get user full name matching username passed """
        user = cls.query.filter(User.username == username).one_or_none()
        if user:
            first_name = user.first_name
            last_name = user.last_name
            return f"{first_name} {last_name}"
        else:
            return None

    # @classmethod
    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already registered.')

from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.utils import secure_filename


class RegUserForm(FlaskForm):
    """Form for reg user."""

    username = StringField(
        "User name", validators=[
            InputRequired(message="Username requiered must be unique"),
            Length(max=20, message="Max length is 20 characters")
        ]
    )
    first_name = StringField(
        "First name", validators=[
            InputRequired(message="Username requiered"),
            Length(min=1, max=30, message="Max length is 30 characters")
        ]
    )
    last_name = StringField(
        "Last name", validators=[
            InputRequired(message="Username requiered"),
            Length(min=1, max=30, message="Max length is 30 characters")
        ]
    )
    password = PasswordField(
        'Password', validators=[
            InputRequired(message="Password Required"),
            Length(min=6, max=50, message="min = 6, max length 50")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(
                message="Email validation failed...",
                granular_message=True,
                check_deliverability=True,
                allow_smtputf8=True,
                allow_empty_local=False
            ),
            Length(min=6, max=50, message="min = 6, max length 50")],
    )


# images = UploadSet('images', IMAGES)


# class UploadForm(FlaskForm):
#     upload = FileField('image', validators=[
#         FileRequired(message="Plese use a vaild file"),
#         FileAllowed(images, message='Images only!')
#     ])

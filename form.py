from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename


class RegUserForm(FlaskForm):
    """Form for reg user."""

    username = StringField(
        "User name", validators=[InputRequired(message="Username requiered must be unique")]
    )


# images = UploadSet('images', IMAGES)


# class UploadForm(FlaskForm):
#     upload = FileField('image', validators=[
#         FileRequired(message="Plese use a vaild file"),
#         FileAllowed(images, message='Images only!')
#     ])

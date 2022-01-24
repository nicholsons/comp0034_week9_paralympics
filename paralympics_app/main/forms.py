from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from paralympics_app import photos
from paralympics_app.models import Profile


class ProfileForm(FlaskForm):
    """ Class for the profile form"""
    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    bio = TextAreaField(label='Bio', description='Write something about yourself')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    region_id = SelectField(label='Select your paralympic region', coerce=int)

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile is not None:
            raise ValidationError('Username already exists, please choose another username')


class CompetitionForm(FlaskForm):
    """ Class for the competition entries
    TODO: Create select rather than text entry. Add more questions based on Dashboard data.
    """
    q1 = StringField(label='In which city was the first paralympic event held?', validators=[DataRequired(
        message='Answer is required')])
    q2 = StringField(label='Which country won the most gold medals in Salt Lake City in 2002', validators=[DataRequired(
        message='Answer is required')])

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, TextAreaField

from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UploadForm(FlaskForm):
    video_title = StringField('Title', validators=[DataRequired()])
    video_link = StringField('Link', validators=[DataRequired()], render_kw={'placeholder':"https://www.youtube.com/watch?v="})
    video_description = TextAreaField('Description')
    submit = SubmitField('Submit')
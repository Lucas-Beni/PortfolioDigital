from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateField, URLField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, URL, Email, EqualTo, ValidationError
from models import Category, User

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    content = TextAreaField('Detailed Content', validators=[Optional()])
    image = FileField('Project Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    demo_url = URLField('Demo URL', validators=[Optional(), URL()])
    github_url = URLField('GitHub URL', validators=[Optional(), URL()])
    technologies = StringField('Technologies (comma-separated)', validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    is_published = BooleanField('Published')
    is_featured = BooleanField('Featured')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(0, 'No Category')] + [(c.id, c.name) for c in Category.query.all()]

class AchievementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    date_achieved = DateField('Date Achieved', validators=[DataRequired()])
    image = FileField('Achievement Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    certificate_url = URLField('Certificate URL', validators=[Optional(), URL()])
    organization = StringField('Organization', validators=[Optional(), Length(max=200)])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    is_published = BooleanField('Published')

    def __init__(self, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(0, 'No Category')] + [(c.id, c.name) for c in Category.query.all()]

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    color = StringField('Color', validators=[DataRequired()], default='#007bff')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=1000)])

class AboutMeForm(FlaskForm):
    content = TextAreaField('About Me Content', validators=[DataRequired()])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    resume_url = URLField('Resume URL', validators=[Optional(), URL()])
    linkedin_url = URLField('LinkedIn URL', validators=[Optional(), URL()])
    github_url = URLField('GitHub URL', validators=[Optional(), URL()])
    website_url = URLField('Website URL', validators=[Optional(), URL()])

# Authentication Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class ShareForm(FlaskForm):
    message = TextAreaField('Personal Message', validators=[Optional(), Length(max=500)])

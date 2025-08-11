from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL
from models import Category

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

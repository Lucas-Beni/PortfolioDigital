from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import current_user, login_user, logout_user
from sqlalchemy import desc, or_
from datetime import datetime
import urllib.parse

from app import app, db
from auth_decorators import login_required, admin_required
from models import User, Project, Achievement, Category, Comment, Like, AboutMe, Education
from forms import ProjectForm, AchievementForm, CategoryForm, CommentForm, AboutMeForm, LoginForm, RegisterForm, ShareForm, EducationForm
from utils import save_uploaded_file, delete_file
from translations import get_translation

# Register authentication blueprint

# Make session permanent and set language
@app.before_request
def make_session_permanent():
    session.permanent = True
    
    # Set language from session or default to English
    if 'language' not in session:
        session['language'] = 'en'

# Language switching route
@app.route('/set_language/<language>')
def set_language(language):
    """Set the language preference"""
    if language in ['en', 'pt']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

# Template context processor for translations
@app.context_processor
def inject_translations():
    """Make translation function available in all templates"""
    def t(key):
        lang = session.get('language', 'en')
        return get_translation(key, lang)
    
    return dict(t=t, current_language=session.get('language', 'en'))

# Authentication Routes (Local Login/Register)
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Local login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Local registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.create_local_user(
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
def logout():
    """Logout for local users"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Public Routes
@app.route('/')
def index():
    """Homepage showing featured projects and certifications"""
    featured_projects = Project.query.filter_by(is_published=True, is_featured=True).limit(6).all()
    featured_certifications = Achievement.query.filter_by(is_published=True, is_featured=True).limit(4).all()
    
    # Get about me info for homepage
    about_me = AboutMe.query.first()
    
    return render_template('index.html', 
                         featured_projects=featured_projects,
                         featured_certifications=featured_certifications,
                         about_me=about_me)

@app.route('/projects')
def projects():
    """View all published projects with filtering"""
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '').strip()
    
    query = Project.query.filter_by(is_published=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(or_(
            Project.title.contains(search),
            Project.description.contains(search),
            Project.technologies.contains(search)
        ))
    
    projects = query.order_by(desc(Project.created_at)).all()
    categories = Category.query.all()
    
    return render_template('projects.html', 
                         projects=projects, 
                         categories=categories,
                         selected_category=category_id,
                         search_term=search)

@app.route('/project/<int:id>')
def project_detail(id):
    """View individual project with comments"""
    project = Project.query.get_or_404(id)
    
    if not project.is_published:
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Project not found.', 'error')
            return redirect(url_for('projects'))
    
    comments = Comment.query.filter_by(project_id=id, is_approved=True).order_by(Comment.created_at).all()
    comment_form = CommentForm()
    
    return render_template('project_detail.html', 
                         project=project, 
                         comments=comments,
                         comment_form=comment_form)

@app.route('/achievements')
def achievements():
    """View all published achievements"""
    category_id = request.args.get('category', type=int)
    
    query = Achievement.query.filter_by(is_published=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    achievements = query.order_by(desc(Achievement.date_achieved)).all()
    categories = Category.query.all()
    
    return render_template('achievements.html', 
                         achievements=achievements, 
                         categories=categories,
                         selected_category=category_id)

@app.route('/about')
def about():
    """About me page"""
    about_me = AboutMe.query.first()
    if not about_me:
        about_me = AboutMe()
        about_me.content = "Welcome to my portfolio! More information coming soon."
    
    return render_template('about.html', about_me=about_me)

# Interactive Routes (require login)
@app.route('/project/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    """Add comment to project"""
    project = Project.query.get_or_404(id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment()
        comment.content = form.content.data
        comment.user_id = current_user.id
        comment.project_id = id
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    else:
        flash('Error adding comment. Please try again.', 'error')
    
    return redirect(url_for('project_detail', id=id))

@app.route('/project/<int:id>/like', methods=['POST'])
@login_required
def toggle_like(id):
    """Toggle like for project"""
    project = Project.query.get_or_404(id)
    
    existing_like = Like.query.filter_by(user_id=current_user.id, project_id=id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        like = Like()
        like.user_id = current_user.id
        like.project_id = id
        db.session.add(like)
        liked = True
    
    db.session.commit()
    
    return jsonify({
        'liked': liked,
        'like_count': project.like_count
    })

# LinkedIn Sharing Route
@app.route('/project/<int:id>/share', methods=['GET', 'POST'])
@login_required
def share_project(id):
    """Share project on LinkedIn with personalized message"""
    project = Project.query.get_or_404(id)
    
    if not project.is_published:
        flash('Project not available for sharing.', 'error')
        return redirect(url_for('projects'))
    
    form = ShareForm()
    
    if form.validate_on_submit():
        # Generate LinkedIn sharing URL
        project_url = url_for('project_detail', id=project.id, _external=True)
        
        # Create sharing message
        share_text = f"Check out this amazing project: {project.title}\n\n{project.description}"
        if form.message.data:
            share_text += f"\n\nPersonal note: {form.message.data}"
        
        share_text += f"\n\n#portfolio #webdevelopment"
        if project.technologies:
            techs = [tech.strip().replace(' ', '').lower() for tech in project.technologies.split(',')][:3]
            for tech in techs:
                share_text += f" #{tech}"
        
        # LinkedIn sharing URL (modern approach)
        linkedin_params = {
            'url': project_url,
            'text': share_text
        }
        
        linkedin_url = 'https://www.linkedin.com/feed/?' + urllib.parse.urlencode(linkedin_params)
        
        return redirect(linkedin_url)
    
    return render_template('share_project.html', project=project, form=form)

# Admin Routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    stats = {
        'projects': Project.query.count(),
        'published_projects': Project.query.filter_by(is_published=True).count(),
        'achievements': Achievement.query.count(),
        'categories': Category.query.count(),
        'comments': Comment.query.count(),
        'likes': Like.query.count(),
        'education': Education.query.count()
    }
    
    recent_comments = Comment.query.order_by(desc(Comment.created_at)).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_comments=recent_comments)

@app.route('/admin/projects')
@admin_required
def admin_projects():
    """Admin projects list"""
    projects = Project.query.order_by(desc(Project.created_at)).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/new', methods=['GET', 'POST'])
@admin_required
def admin_project_new():
    """Create new project"""
    form = ProjectForm()
    
    if form.validate_on_submit():
        project = Project()
        project.title = form.title.data
        project.description = form.description.data
        project.content = form.content.data
        project.deployed_url = form.deployed_url.data
        project.github_url = form.github_url.data
        project.technologies = form.technologies.data
        project.category_id = form.category_id.data if form.category_id.data != 0 else None
        project.is_published = form.is_published.data
        project.is_featured = form.is_featured.data
        
        # Handle file upload
        if form.image.data:
            filename = save_uploaded_file(form.image.data, 'projects')
            if filename:
                project.image_url = filename
        
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', form=form, title='New Project')

@app.route('/admin/projects/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_project_edit(id):
    """Edit project"""
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        old_image = project.image_url
        
        form.populate_obj(project)
        project.category_id = form.category_id.data if form.category_id.data != 0 else None
        project.updated_at = datetime.now()
        
        # Handle file upload
        if form.image.data:
            filename = save_uploaded_file(form.image.data, 'projects')
            if filename:
                if old_image:
                    delete_file(old_image)
                project.image_url = filename
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', form=form, project=project, title='Edit Project')

@app.route('/admin/projects/<int:id>/delete', methods=['POST'])
@admin_required
def admin_project_delete(id):
    """Delete project"""
    project = Project.query.get_or_404(id)
    
    # Delete associated image
    if project.image_url:
        delete_file(project.image_url)
    
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/achievements')
@admin_required
def admin_achievements():
    """Admin achievements list"""
    achievements = Achievement.query.order_by(desc(Achievement.date_achieved)).all()
    return render_template('admin/achievements.html', achievements=achievements)

@app.route('/admin/achievements/new', methods=['GET', 'POST'])
@admin_required
def admin_achievement_new():
    """Create new achievement"""
    form = AchievementForm()
    
    if form.validate_on_submit():
        achievement = Achievement()
        achievement.title = form.title.data
        achievement.description = form.description.data
        achievement.date_achieved = form.date_achieved.data
        achievement.certificate_url = form.certificate_url.data
        achievement.organization = form.organization.data
        achievement.category_id = form.category_id.data if form.category_id.data != 0 else None
        achievement.is_published = form.is_published.data
        achievement.is_featured = form.is_featured.data
        
        # Handle file upload
        if form.image.data:
            filename = save_uploaded_file(form.image.data, 'achievements')
            if filename:
                achievement.image_url = filename
        
        db.session.add(achievement)
        db.session.commit()
        flash('Achievement created successfully!', 'success')
        return redirect(url_for('admin_achievements'))
    
    return render_template('admin/achievement_form.html', form=form, title='New Achievement')

@app.route('/admin/achievements/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_achievement_edit(id):
    """Edit achievement"""
    achievement = Achievement.query.get_or_404(id)
    form = AchievementForm(obj=achievement)
    
    if form.validate_on_submit():
        old_image = achievement.image_url
        
        form.populate_obj(achievement)
        achievement.category_id = form.category_id.data if form.category_id.data != 0 else None
        achievement.updated_at = datetime.now()
        
        # Handle file upload
        if form.image.data:
            filename = save_uploaded_file(form.image.data, 'achievements')
            if filename:
                if old_image:
                    delete_file(old_image)
                achievement.image_url = filename
        
        db.session.commit()
        flash('Achievement updated successfully!', 'success')
        return redirect(url_for('admin_achievements'))
    
    return render_template('admin/achievement_form.html', form=form, achievement=achievement, title='Edit Achievement')

@app.route('/admin/achievements/<int:id>/delete', methods=['POST'])
@admin_required
def admin_achievement_delete(id):
    """Delete achievement"""
    achievement = Achievement.query.get_or_404(id)
    
    # Delete associated image
    if achievement.image_url:
        delete_file(achievement.image_url)
    
    db.session.delete(achievement)
    db.session.commit()
    flash('Achievement deleted successfully!', 'success')
    return redirect(url_for('admin_achievements'))

@app.route('/admin/categories')
@admin_required
def admin_categories():
    """Admin categories list"""
    categories = Category.query.all()
    form = CategoryForm()
    return render_template('admin/categories.html', categories=categories, form=form)

@app.route('/admin/categories/new', methods=['POST'])
@admin_required
def admin_category_new():
    """Create new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category()
        category.name = form.name.data
        category.color = form.color.data
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
    else:
        flash('Error creating category.', 'error')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/<int:id>/delete', methods=['POST'])
@admin_required
def admin_category_delete(id):
    """Delete category"""
    category = Category.query.get_or_404(id)
    
    # Check if category is in use
    if category.projects.count() > 0 or category.achievements.count() > 0:
        flash('Cannot delete category that is in use.', 'error')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/about', methods=['GET', 'POST'])
@admin_required
def admin_about_edit():
    """Edit about me section"""
    about_me = AboutMe.query.first()
    if not about_me:
        about_me = AboutMe()
        about_me.content = ""
    
    form = AboutMeForm(obj=about_me)
    
    if form.validate_on_submit():
        old_image = about_me.profile_image
        
        form.populate_obj(about_me)
        about_me.updated_at = datetime.now()
        
        # Handle file upload
        if form.profile_image.data:
            filename = save_uploaded_file(form.profile_image.data, 'profile')
            if filename:
                if old_image:
                    delete_file(old_image)
                about_me.profile_image = filename
        
        if about_me.id:
            db.session.commit()
        else:
            db.session.add(about_me)
            db.session.commit()
        
        flash('About section updated successfully!', 'success')
        return redirect(url_for('admin_about_edit'))
    
    return render_template('admin/about_edit.html', form=form, about_me=about_me)

# GitHub Sync Route
@app.route('/admin/sync-github')
@admin_required
def admin_sync_github():
    """Sync projects from GitHub"""
    from github_sync import sync_github_projects
    
    result = sync_github_projects()
    
    if result['success']:
        flash(f"GitHub sincronizado! {result['synced']} novos projetos, {result.get('updated', 0)} atualizados.", 'success')
    else:
        flash(f"Erro ao sincronizar GitHub: {result['message']}", 'error')
    
    return redirect(url_for('admin_projects'))

# Education Admin Routes
@app.route('/admin/education')
@admin_required
def admin_education():
    """Admin education list"""
    education_list = Education.query.order_by(desc(Education.start_date)).all()
    return render_template('admin/education.html', education_list=education_list)

@app.route('/admin/education/new', methods=['GET', 'POST'])
@admin_required
def admin_education_new():
    """Create new education entry"""
    form = EducationForm()
    
    if form.validate_on_submit():
        education = Education()
        education.institution = form.institution.data
        education.degree = form.degree.data
        education.field_of_study = form.field_of_study.data
        education.start_date = form.start_date.data
        education.end_date = form.end_date.data
        education.is_current = form.is_current.data
        education.description = form.description.data
        education.location = form.location.data
        education.is_published = form.is_published.data
        
        db.session.add(education)
        db.session.commit()
        flash('Formação acadêmica adicionada com sucesso!', 'success')
        return redirect(url_for('admin_education'))
    
    return render_template('admin/education_form.html', form=form, title='Nova Formação')

@app.route('/admin/education/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_education_edit(id):
    """Edit education entry"""
    education = Education.query.get_or_404(id)
    form = EducationForm(obj=education)
    
    if form.validate_on_submit():
        form.populate_obj(education)
        education.updated_at = datetime.now()
        
        db.session.commit()
        flash('Formação acadêmica atualizada com sucesso!', 'success')
        return redirect(url_for('admin_education'))
    
    return render_template('admin/education_form.html', form=form, education=education, title='Editar Formação')

@app.route('/admin/education/<int:id>/delete', methods=['POST'])
@admin_required
def admin_education_delete(id):
    """Delete education entry"""
    education = Education.query.get_or_404(id)
    
    db.session.delete(education)
    db.session.commit()
    flash('Formação acadêmica excluída com sucesso!', 'success')
    return redirect(url_for('admin_education'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

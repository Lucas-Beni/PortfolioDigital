from functools import wraps
from flask import redirect, url_for, session, request
from flask_login import current_user

def login_required(f):
    """Decorator for routes that require login (works with both local and Replit auth)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            session["next_url"] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for routes that require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            session["next_url"] = request.url
            return redirect(url_for('login'))
        
        if not current_user.is_admin:
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function
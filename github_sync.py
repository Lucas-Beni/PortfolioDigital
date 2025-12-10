"""
GitHub Sync Module for Portfolio
Fetches repositories from Lucas-Beni GitHub profile and syncs them to the database
Uses Replit's GitHub connector integration
"""
import os
import json
import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

GITHUB_USERNAME = "Lucas-Beni"

connection_settings = None

def get_access_token():
    """Get GitHub access token from Replit connector"""
    global connection_settings
    
    if connection_settings and connection_settings.get('settings', {}).get('expires_at'):
        expires_at = connection_settings['settings']['expires_at']
        if datetime.fromisoformat(expires_at.replace('Z', '+00:00')) > datetime.now():
            return connection_settings['settings'].get('access_token')
    
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    repl_identity = os.environ.get('REPL_IDENTITY')
    web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
    
    if repl_identity:
        x_replit_token = f'repl {repl_identity}'
    elif web_repl_renewal:
        x_replit_token = f'depl {web_repl_renewal}'
    else:
        logger.warning("No Replit token found, will use public API")
        return None
    
    if not hostname:
        logger.warning("No connector hostname found")
        return None
    
    try:
        response = requests.get(
            f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=github',
            headers={
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            connection_settings = data.get('items', [{}])[0] if data.get('items') else {}
            
            access_token = (
                connection_settings.get('settings', {}).get('access_token') or
                connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
            )
            
            if access_token:
                return access_token
                
    except Exception as e:
        logger.error(f"Error getting access token: {e}")
    
    return None

def fetch_github_repos(username=GITHUB_USERNAME):
    """Fetch public repositories from GitHub"""
    access_token = get_access_token()
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Portfolio-App'
    }
    
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    
    try:
        url = f'https://api.github.com/users/{username}/repos'
        params = {
            'sort': 'updated',
            'direction': 'desc',
            'per_page': 100
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            repos = response.json()
            logger.info(f"Fetched {len(repos)} repositories from GitHub")
            return repos
        else:
            logger.error(f"GitHub API error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        logger.error(f"Error fetching repos: {e}")
        return []

def get_repo_languages(username, repo_name, headers):
    """Get languages used in a repository"""
    try:
        url = f'https://api.github.com/repos/{username}/{repo_name}/languages'
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            languages = response.json()
            return list(languages.keys())
        return []
    except Exception as e:
        logger.error(f"Error fetching languages for {repo_name}: {e}")
        return []

def sync_github_projects():
    """Sync GitHub repositories to the database as projects"""
    from app import db
    from models import Project
    
    repos = fetch_github_repos(GITHUB_USERNAME)
    
    if not repos:
        return {'success': False, 'message': 'No repositories found or API error', 'synced': 0}
    
    access_token = get_access_token()
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Portfolio-App'
    }
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    
    synced_count = 0
    updated_count = 0
    
    for repo in repos:
        if repo.get('fork') or repo.get('private'):
            continue
        
        github_url = repo.get('html_url', '')
        
        existing_project = Project.query.filter_by(github_url=github_url).first()
        
        languages = get_repo_languages(GITHUB_USERNAME, repo['name'], headers)
        topics = repo.get('topics', [])
        technologies = ', '.join(languages + topics) if languages or topics else repo.get('language', '')
        
        description = repo.get('description') or f"Repository: {repo['name']}"
        
        if existing_project:
            existing_project.title = repo['name']
            existing_project.description = description[:500]
            existing_project.technologies = technologies
            existing_project.demo_url = repo.get('homepage') or ''
            existing_project.updated_at = datetime.now()
            updated_count += 1
        else:
            new_project = Project()
            new_project.title = repo['name']
            new_project.description = description[:500]
            new_project.content = f"This project was automatically imported from GitHub.\n\nRepository: {github_url}\n\nDescription: {description}"
            new_project.github_url = github_url
            new_project.demo_url = repo.get('homepage') or ''
            new_project.technologies = technologies
            new_project.is_published = True
            new_project.is_featured = repo.get('stargazers_count', 0) >= 1
            
            db.session.add(new_project)
            synced_count += 1
    
    try:
        db.session.commit()
        logger.info(f"GitHub sync complete: {synced_count} new, {updated_count} updated")
        return {
            'success': True,
            'message': f'Synced {synced_count} new projects, updated {updated_count} existing',
            'synced': synced_count,
            'updated': updated_count
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error during sync: {e}")
        return {'success': False, 'message': str(e), 'synced': 0}

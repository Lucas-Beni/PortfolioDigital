# Portfolio Application

## Overview

This is a Flask-based portfolio web application designed to showcase projects, achievements, and personal information. The application features a clean, modern interface with Bootstrap styling and includes both public-facing pages and an admin panel for content management. It supports user authentication through Replit's OAuth system and provides comprehensive CRUD operations for managing portfolio content.

## User Preferences

Preferred communication style: Simple, everyday language.
Language Features: Portuguese/English translation system implemented.
User requested: Translation system for PT/EN and LinkedIn sharing functionality.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap with Replit's dark theme
- **Responsive Design**: Mobile-first approach with Bootstrap grid system
- **JavaScript**: Vanilla JavaScript for enhanced user interactions
- **Static Assets**: CSS and JavaScript files served from static directory
- **Image Handling**: PIL (Pillow) for image processing and optimization
- **Internationalization**: Translation system supporting Portuguese and English
- **Social Sharing**: LinkedIn integration with custom messaging

### Backend Architecture
- **Web Framework**: Flask with modular blueprint structure
- **Database ORM**: SQLAlchemy with declarative base model
- **Authentication**: Flask-Login with Replit OAuth integration
- **Form Handling**: WTForms with Flask-WTF for CSRF protection
- **File Uploads**: Secure file handling with image optimization
- **Session Management**: Flask sessions with permanent session configuration

### Data Models
- **User Management**: User model with admin privileges and OAuth integration
- **Content Models**: Project, Achievement, Category, Comment, Like, and AboutMe models
- **Relationships**: Proper foreign key relationships between entities
- **Timestamps**: Automatic created_at and updated_at tracking

### Authentication & Authorization
- **OAuth Provider**: Replit authentication system
- **Session Storage**: Database-backed OAuth token storage
- **Access Control**: Decorator-based admin and login requirements
- **User Roles**: Admin flag for privileged operations

### File Management
- **Upload Processing**: Secure filename generation with UUID
- **Image Optimization**: Automatic resizing and compression
- **Storage Structure**: Organized upload directory with subfolders
- **File Validation**: Extension and type checking for security

### Admin Panel Features
- **Dashboard**: Statistics overview and quick access
- **Content Management**: Full CRUD for projects, achievements, and categories
- **Profile Management**: About section and personal information editing
- **Publication Control**: Draft/publish workflow for content

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **SQLAlchemy**: Database ORM and connection management
- **Flask-Login**: User session management
- **Flask-Dance**: OAuth integration handling

### Form and Validation
- **WTForms**: Form rendering and validation
- **Flask-WTF**: CSRF protection and file upload handling

### Image Processing
- **Pillow (PIL)**: Image manipulation and optimization

### Frontend Libraries
- **Bootstrap**: CSS framework with Replit dark theme
- **Font Awesome**: Icon library for UI elements

### Database
- **PostgreSQL**: Primary database (configured via DATABASE_URL environment variable)
- **Connection Pooling**: SQLAlchemy engine with pool recycling and pre-ping

### Authentication Services
- **Replit OAuth**: Third-party authentication provider
- **JWT**: Token handling for authentication

### Environment Configuration
- **SESSION_SECRET**: Session encryption key
- **DATABASE_URL**: PostgreSQL connection string
- **Upload directory**: Static file storage for images
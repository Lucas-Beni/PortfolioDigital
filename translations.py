"""
Translation system for the portfolio application
Supports Portuguese and English languages
"""

# Translation dictionaries
translations = {
    'en': {
        # Navigation
        'nav_home': 'Home',
        'nav_projects': 'Projects',
        'nav_achievements': 'Achievements', 
        'nav_about': 'About',
        'nav_admin': 'Admin',
        'nav_login': 'Login',
        'nav_logout': 'Logout',
        'nav_register': 'Create Account',
        'nav_email_login': 'Email Login',
        'nav_replit_login': 'Continue with Replit',
        
        # Homepage
        'hero_title': 'Welcome to My Portfolio',
        'hero_subtitle': 'Showcasing my projects, achievements, and professional journey',
        'featured_projects': 'Featured Projects',
        'recent_projects': 'Recent Projects',
        'view_all_projects': 'View All Projects',
        'view_project': 'View Project',
        'no_projects': 'No projects available yet.',
        
        # Projects
        'projects_title': 'My Projects',
        'project_demo': 'Live Demo',
        'project_code': 'View Code',
        'project_share': 'Share',
        'project_like': 'Like',
        'project_liked': 'Liked',
        'project_comments': 'Comments',
        'technologies_used': 'Technologies Used',
        'project_details': 'Project Details',
        'add_comment': 'Add Comment',
        'share_linkedin': 'Share on LinkedIn',
        
        # Achievements
        'achievements_title': 'My Achievements',
        'achievement_date': 'Date Achieved',
        'achievement_organization': 'Organization',
        'view_certificate': 'View Certificate',
        'no_achievements': 'No achievements available yet.',
        
        # About
        'about_title': 'About Me',
        'contact_info': 'Contact Information',
        'download_resume': 'Download Resume',
        'linkedin_profile': 'LinkedIn Profile',
        'github_profile': 'GitHub Profile',
        'website_link': 'Website',
        
        # Forms
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'search': 'Search',
        'search_placeholder': 'Search projects...',
        'email': 'Email',
        'password': 'Password',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'message': 'Message',
        'comment': 'Comment',
        
        # Admin
        'admin_dashboard': 'Dashboard',
        'manage_projects': 'Manage Projects',
        'manage_achievements': 'Manage Achievements',
        'manage_categories': 'Categories',
        'edit_about': 'Edit About',
        'add_project': 'Add Project',
        'add_achievement': 'Add Achievement',
        'add_category': 'Add Category',
        
        # Messages
        'login_success': 'Login successful!',
        'logout_success': 'You have been logged out.',
        'registration_success': 'Registration successful! You can now log in.',
        'invalid_credentials': 'Invalid email or password.',
        'project_saved': 'Project saved successfully!',
        'achievement_saved': 'Achievement saved successfully!',
        'comment_added': 'Comment added successfully!',
        'like_added': 'Project liked!',
        'like_removed': 'Like removed',
        'copied_clipboard': 'Copied to clipboard!',
        'share_success': 'Shared successfully!',
        
        # Footer
        'footer_rights': 'All rights reserved.',
        'footer_built_with': 'Built with',
        
        # Language
        'language': 'Language',
        'english': 'English',
        'portuguese': 'Português',
    },
    'pt': {
        # Navigation
        'nav_home': 'Início',
        'nav_projects': 'Projetos',
        'nav_achievements': 'Conquistas',
        'nav_about': 'Sobre',
        'nav_admin': 'Administração',
        'nav_login': 'Entrar',
        'nav_logout': 'Sair',
        'nav_register': 'Criar Conta',
        'nav_email_login': 'Login por Email',
        'nav_replit_login': 'Continuar com Replit',
        
        # Homepage
        'hero_title': 'Bem-vindo ao Meu Portfólio',
        'hero_subtitle': 'Mostrando meus projetos, conquistas e jornada profissional',
        'featured_projects': 'Projetos em Destaque',
        'recent_projects': 'Projetos Recentes',
        'view_all_projects': 'Ver Todos os Projetos',
        'view_project': 'Ver Projeto',
        'no_projects': 'Nenhum projeto disponível ainda.',
        
        # Projects
        'projects_title': 'Meus Projetos',
        'project_demo': 'Demo ao Vivo',
        'project_code': 'Ver Código',
        'project_share': 'Compartilhar',
        'project_like': 'Curtir',
        'project_liked': 'Curtido',
        'project_comments': 'Comentários',
        'technologies_used': 'Tecnologias Utilizadas',
        'project_details': 'Detalhes do Projeto',
        'add_comment': 'Adicionar Comentário',
        'share_linkedin': 'Compartilhar no LinkedIn',
        
        # Achievements
        'achievements_title': 'Minhas Conquistas',
        'achievement_date': 'Data da Conquista',
        'achievement_organization': 'Organização',
        'view_certificate': 'Ver Certificado',
        'no_achievements': 'Nenhuma conquista disponível ainda.',
        
        # About
        'about_title': 'Sobre Mim',
        'contact_info': 'Informações de Contato',
        'download_resume': 'Baixar Currículo',
        'linkedin_profile': 'Perfil do LinkedIn',
        'github_profile': 'Perfil do GitHub',
        'website_link': 'Website',
        
        # Forms
        'submit': 'Enviar',
        'cancel': 'Cancelar',
        'save': 'Salvar',
        'edit': 'Editar',
        'delete': 'Excluir',
        'search': 'Pesquisar',
        'search_placeholder': 'Pesquisar projetos...',
        'email': 'Email',
        'password': 'Senha',
        'first_name': 'Nome',
        'last_name': 'Sobrenome',
        'message': 'Mensagem',
        'comment': 'Comentário',
        
        # Admin
        'admin_dashboard': 'Painel de Controle',
        'manage_projects': 'Gerenciar Projetos',
        'manage_achievements': 'Gerenciar Conquistas',
        'manage_categories': 'Categorias',
        'edit_about': 'Editar Sobre',
        'add_project': 'Adicionar Projeto',
        'add_achievement': 'Adicionar Conquista',
        'add_category': 'Adicionar Categoria',
        'new_project': 'Novo Projeto',
        'new_achievement': 'Nova Conquista',
        'categories': 'Categorias',
        'dashboard': 'Painel',
        'statistics': 'Estatísticas',
        'total_projects': 'Total de Projetos',
        'total_achievements': 'Total de Conquistas',
        'published_projects': 'Projetos Publicados',
        'recent_comments': 'Comentários Recentes',
        
        # Messages
        'login_success': 'Login realizado com sucesso!',
        'logout_success': 'Você foi desconectado.',
        'registration_success': 'Registro realizado com sucesso! Agora você pode fazer login.',
        'invalid_credentials': 'Email ou senha inválidos.',
        'project_saved': 'Projeto salvo com sucesso!',
        'achievement_saved': 'Conquista salva com sucesso!',
        'comment_added': 'Comentário adicionado com sucesso!',
        'like_added': 'Projeto curtido!',
        'like_removed': 'Curtida removida',
        'copied_clipboard': 'Copiado para a área de transferência!',
        'share_success': 'Compartilhado com sucesso!',
        
        # Footer
        'footer_rights': 'Todos os direitos reservados.',
        'footer_built_with': 'Desenvolvido com',
        
        # Language
        'language': 'Idioma',
        'english': 'English',
        'portuguese': 'Português',
    }
}

def get_translation(key, lang='en'):
    """Get translation for a given key and language"""
    return translations.get(lang, {}).get(key, translations['en'].get(key, key))

def t(key, lang='en'):
    """Shorthand for get_translation"""
    return get_translation(key, lang)
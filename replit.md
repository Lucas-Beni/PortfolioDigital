# Portfolio Digital - Lucas Beni

## Visão Geral
Site de portfólio pessoal com estilo hacker/terminal, suporte bilíngue (Português/Inglês), e integração com GitHub para sincronização automática de projetos.

## Características Principais
- **Design Hacker/Terminal**: Interface estilizada com tema verde matrix/terminal
- **Bilíngue**: Suporte completo para Português e Inglês
- **Sincronização GitHub**: Importação automática de repositórios do GitHub
- **Sistema de Projetos**: CRUD completo para projetos com categorias
- **Sistema de Conquistas**: CRUD completo para conquistas/certificados
- **Comentários e Likes**: Interação social nos projetos
- **Compartilhamento**: Integração com LinkedIn e Twitter

## Credenciais de Admin
- **Email**: admin@portfolio.com
- **Senha**: admin123

## Estrutura do Projeto
```
├── app.py              # Configuração principal Flask
├── main.py             # Entry point
├── routes.py           # Todas as rotas do app
├── models.py           # Modelos do banco de dados
├── forms.py            # Formulários WTForms
├── translations.py     # Sistema de tradução PT/EN
├── github_sync.py      # Sincronização com GitHub
├── templates/          # Templates Jinja2
│   ├── base.html       # Template base
│   ├── index.html      # Homepage
│   ├── projects.html   # Lista de projetos
│   ├── achievements.html # Lista de conquistas
│   ├── about.html      # Página sobre
│   ├── auth/           # Login e registro
│   └── admin/          # Painel administrativo
└── static/
    ├── css/custom.css  # Estilos personalizados
    └── js/main.js      # JavaScript
```

## Tecnologias
- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, Font Awesome, Fira Code
- **Banco de Dados**: SQLite (desenvolvimento)
- **Integração**: GitHub API via Replit Connector

## Rotas Principais
- `/` - Homepage
- `/projects` - Lista de projetos
- `/achievements` - Lista de conquistas
- `/about` - Sobre mim
- `/login` - Login
- `/register` - Registro
- `/admin` - Painel administrativo
- `/admin/sync-github` - Sincronizar projetos do GitHub

## Preferências do Usuário
- Idioma preferido: Português
- Estilo visual: Hacker/Terminal com tema verde matrix
- GitHub: https://github.com/Lucas-Beni

## Mudanças Recentes (Dezembro 2025)
- Implementado sistema completo de tradução PT/EN
- Adicionada sincronização automática com GitHub
- Melhorado design hacker com efeitos visuais
- Criado novo usuário admin
- Atualizado todos os templates para usar traduções

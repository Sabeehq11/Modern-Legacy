# Modern-Legacy Django Project

Modern-Legacy contains a large legacy Django 1.8 codebase (edX platform from 2016) alongside a modern Django 4.2 demo application for comparison and analysis of technical debt evolution.

## ⚠️ CRITICAL RULE: NEVER MODIFY THE LEGACY-EDX FOLDER

**The `legacy-edx/` folder is a historical reference and MUST NOT be modified under any circumstances.** This folder contains:
- A snapshot of the edX platform from 2016
- Legacy code for analysis and learning purposes only
- Examples of outdated patterns and technical debt

**Any attempts to update, modernize, or change files in `legacy-edx/` should be redirected to creating new implementations in a separate folder (e.g., `modern-edx/`).**

## Project Structure

```
Modern-Legacy/
├── legacy-edx/              # Legacy edX platform (Django 1.8, ~985K lines)
│   ├── lms/                 # Learning Management System (49 Django apps)
│   ├── cms/                 # Course Management System
│   ├── common/              # Shared Django apps
│   └── openedx/             # Core platform code
├── modern_django_demo/      # Modern Django 4.2 demo app
│   ├── manage.py           # Django management script
│   └── modern_django_demo/ # Project configuration
└── django-demo-env/        # Python virtual environment
```

## Build & Commands

### Modern Django Demo (Django 4.2)
```bash
# Activate virtual environment
source django-demo-env/bin/activate

# Run development server
cd modern_django_demo
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create new app
python manage.py startapp <app_name>

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

### Development URLs
- Modern Django: http://localhost:8000
- Django Admin: http://localhost:8000/admin

### Legacy edX (Reference Only - Not Runnable)
The legacy edX codebase requires Python 2.7 and complex infrastructure:
- MySQL 5.6, MongoDB 2.6, RabbitMQ, Memcached, Elasticsearch
- Use for code analysis and pattern study only

## Code Style

### Django Best Practices
- Use Django 4.2 patterns (path() not url())
- Class-based views preferred over function-based views
- Use Django's built-in authentication
- Follow Django's MVT (Model-View-Template) pattern
- Keep business logic in models or services, not views
- Use Django forms for validation
- Leverage Django's ORM efficiently

### Python Style
- Python 3.10+ with type hints where beneficial
- PEP 8 compliance (4 spaces indentation)
- 79 character line limit for code, 72 for docstrings
- Use descriptive variable/function names
- Docstrings for all public functions/classes
- Import order: standard library, third-party, local
- Use f-strings for formatting (not % or .format())

### Legacy Pattern Examples to Avoid
```python
# DON'T use Django 1.x patterns:
from django.conf.urls import patterns, url
urlpatterns = patterns('',
    url(r'^$', 'views.index'),
)

# DO use modern Django:
from django.urls import path
urlpatterns = [
    path('', views.index, name='index'),
]
```

## Testing

- Use Django's TestCase for database tests
- Use SimpleTestCase for non-database tests
- Test file naming: `test_*.py` or `tests.py`
- One test class per view/model
- Use fixtures for test data
- Mock external services
- Run with: `python manage.py test`

## Architecture Comparison

### Modern Django Demo
- **Django**: 4.2 (latest LTS)
- **Python**: 3.10+
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: Django templates + minimal JS
- **Apps**: Modular, focused (typically 5-10)

### Legacy edX Platform
- **Django**: 1.8.15 (EOL 2018)
- **Python**: 2.7 (EOL 2020)
- **Database**: MySQL + MongoDB
- **Frontend**: Mako templates, RequireJS, Backbone.js
- **Apps**: 49 in LMS alone (monolithic)

## Security

- Keep SECRET_KEY secure and out of version control
- Use environment variables for sensitive data
- Update ALLOWED_HOSTS for production
- Enable CSRF protection (default in Django)
- Use Django's built-in password validators
- Regular security updates via `pip-audit`
- Never store passwords in plain text
- Use Django's make_password() for manual password creation

## Database

### Modern Django
```python
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create migration for specific app
python manage.py makemigrations app_name

# Show migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name 0001
```

### Legacy Patterns to Modernize
- Replace South migrations with Django migrations
- Update model Meta options syntax
- Use model field choices as Enums
- Replace `__unicode__` with `__str__`

## Git Workflow

- NEVER commit `*.pyc` files or `__pycache__/`
- NEVER commit `db.sqlite3` or other databases
- NEVER commit `.env` files with secrets
- Always include migrations in commits
- Run `python manage.py check` before committing
- Use `.gitignore` for Python projects
- Create feature branches for new work
- Write descriptive commit messages

## Configuration

### Environment Setup
```bash
# Create virtual environment
python3 -m venv django-demo-env

# Activate environment
source django-demo-env/bin/activate  # Unix/macOS
# or
django-demo-env\Scripts\activate  # Windows

# Install dependencies
pip install django==4.2
pip install -r requirements.txt
```

### Django Settings
- Development: `DEBUG = True`
- Production: `DEBUG = False`
- Use `python-decouple` for environment variables
- Separate settings files for different environments
- Always update `ALLOWED_HOSTS` for production

## Common Tasks

### Adding a New Feature
1. Create app: `python manage.py startapp feature_name`
2. Add to INSTALLED_APPS in settings.py
3. Define models in models.py
4. Create and run migrations
5. Register models in admin.py
6. Create views and templates
7. Add URL patterns
8. Write tests
9. Document the feature

### Analyzing Legacy Code
1. Look for deprecated patterns in `legacy-edx/`
2. Identify monolithic components
3. Find tightly coupled code
4. Note outdated dependencies
5. Document modernization opportunities

## Resources

- Django 4.2 Docs: https://docs.djangoproject.com/en/4.2/
- Django Style Guide: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
- Python PEP 8: https://www.python.org/dev/peps/pep-0008/
- Django Security: https://docs.djangoproject.com/en/4.2/topics/security/

## Important Notes

- The legacy edX codebase is for analysis only (requires Python 2.7)
- Focus development on the modern Django demo
- Use legacy code to understand technical debt patterns
- Always follow modern Django best practices
- Keep security in mind for all changes 
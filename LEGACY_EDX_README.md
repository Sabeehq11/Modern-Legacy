# Legacy Open edX Platform (2016)

## Overview
This is the **Eucalyptus release** of Open edX from 2016, representing a true legacy Django codebase perfect for Path 3 analysis.

## Key Legacy Characteristics

### Django Version
- **Django 1.8.15** (Released in 2015, EOL in 2018)
- Uses deprecated patterns like `django.conf.urls.patterns`
- Pre-Django 2.0 (before Python 3 support)

### Codebase Statistics
- **Python Code**: 466,494 lines
- **Total Code** (Python, JS, HTML, CSS): 984,658 lines
- **Age**: 8+ years old
- **Last maintained**: 2016-2017

### Legacy Patterns Found
1. **URL Patterns**: Uses deprecated `patterns()` function
   ```python
   from django.conf.urls import patterns, url
   urlpatterns = patterns('',
       url(r'^$', 'views.index'),
   )
   ```

2. **Old Middleware**: Uses `MIDDLEWARE_CLASSES` instead of `MIDDLEWARE`
3. **South Migrations**: Pre-Django 1.7 migration system remnants
4. **Function-based views**: Heavy use of FBVs over CBVs
5. **Old template syntax**: `{% load url from future %}`

### Major Components
- **LMS** (Learning Management System): Student-facing platform
- **CMS** (Studio): Course authoring system
- **Common**: Shared Django apps
- **OpenEdX**: Core platform code

### Technology Stack
- Python 2.7 (not Python 3 compatible)
- Django 1.8.15
- Celery 3.1.16
- MySQL/MongoDB
- Mako templates (instead of Django templates)
- RequireJS for JavaScript modules
- Backbone.js for frontend

### Why This is Perfect for Path 3
1. **Large Scale**: Nearly 1 million lines of code
2. **Enterprise Complexity**: Used by MIT, Harvard, Stanford
3. **Technical Debt**: 8+ years of accumulated patterns
4. **Deprecated Technologies**: Django 1.8, Python 2.7
5. **Monolithic Architecture**: Pre-microservices design
6. **Legacy Patterns**: Outdated Django practices throughout

### Running the Legacy System
Due to its age, this requires:
- Python 2.7 (EOL since 2020)
- Ubuntu 14.04 or 16.04
- MySQL 5.6
- MongoDB 2.6
- Memcached
- RabbitMQ

### Common Issues
- Incompatible with modern Python/Django
- Security vulnerabilities in dependencies
- Deprecated authentication methods
- Legacy AJAX patterns
- Old JavaScript tooling

This codebase represents a perfect example of a large-scale legacy Django application that would benefit from modernization. 
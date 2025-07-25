# Ampcode Prompt: Modernize Legacy edX Platform

## Project Overview
Create a modern version of the legacy edX platform called "modern-edx" that maintains the core functionality of the original LMS (Learning Management System) and CMS (Studio) while using modern architecture, tools, and best practices.

## Current Legacy Structure Analysis
The legacy edX platform has:
- **Dual Django Apps**: LMS and CMS (Studio) running as separate Django projects
- **Python 2.7 codebase** with Django 1.8.15
- **Complex configuration**: Multiple environment settings (dev, aws, common, etc.)
- **Monolithic architecture**: Tightly coupled components
- **Legacy dependencies**: Outdated packages and custom forks
- **Custom management**: Uses `manage.py lms` or `manage.py cms` to run different services

## Requirements for Modern edX

### 1. Technology Stack Modernization
- **Python 3.11+** with type hints and modern Python features
- **Django 4.2 LTS** or **Django 5.0** (latest stable)
- **PostgreSQL 15+** as primary database (replace MySQL)
- **Redis** for caching and session storage
- **Celery 5.3+** with Redis as message broker
- **Docker & Docker Compose** for containerization
- **Modern frontend**: React 18+ or Vue 3 for UI components
- **API-first architecture**: Django REST Framework 3.14+
- **GraphQL support** (optional): Graphene-Django for flexible APIs

### 2. Architecture Improvements
- **Microservices-ready**: Separate services that can be deployed independently
- **12-Factor App principles**: Environment-based configuration
- **API Gateway**: Single entry point for all services
- **Event-driven architecture**: Using message queues for async operations
- **Horizontal scalability**: Stateless services that can be scaled

### 3. Project Structure
```
modern-edx/
├── docker/
│   ├── lms/
│   │   └── Dockerfile
│   ├── cms/
│   │   └── Dockerfile
│   └── nginx/
│       ├── Dockerfile
│       └── nginx.conf
├── services/
│   ├── lms/
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   ├── lms/
│   │   │   ├── __init__.py
│   │   │   ├── settings/
│   │   │   │   ├── base.py
│   │   │   │   ├── development.py
│   │   │   │   ├── production.py
│   │   │   │   └── test.py
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   └── asgi.py
│   │   └── apps/
│   │       ├── courses/
│   │       ├── students/
│   │       ├── instructors/
│   │       └── assessments/
│   ├── cms/
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   ├── cms/
│   │   │   ├── __init__.py
│   │   │   ├── settings/
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   └── asgi.py
│   │   └── apps/
│   │       ├── content/
│   │       ├── authoring/
│   │       └── publishing/
│   └── shared/
│       ├── __init__.py
│       ├── authentication/
│       ├── permissions/
│       └── utils/
├── frontend/
│   ├── lms-ui/
│   │   ├── package.json
│   │   ├── src/
│   │   └── public/
│   └── cms-ui/
│       ├── package.json
│       ├── src/
│       └── public/
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .env.example
├── Makefile
└── README.md
```

### 4. Core Features to Implement

#### LMS (Learning Management System)
- **User Management**: Registration, authentication, profiles
- **Course Catalog**: Browse and search courses
- **Course Enrollment**: Enroll in courses, track progress
- **Content Delivery**: Video streaming, documents, interactive content
- **Assessments**: Quizzes, assignments, exams
- **Discussion Forums**: Course-specific discussions
- **Progress Tracking**: Grades, certificates, achievements
- **Mobile API**: RESTful API for mobile apps

#### CMS (Content Management System/Studio)
- **Course Creation**: Create and organize course structure
- **Content Authoring**: Rich text editor, multimedia support
- **Assessment Builder**: Create various types of assessments
- **Publishing Workflow**: Draft, review, publish states
- **Version Control**: Track changes to course content
- **Collaboration**: Multi-author support with permissions
- **Import/Export**: Course portability

### 5. Modern Features to Add
- **Real-time updates**: WebSocket support for live features
- **Advanced Analytics**: Learning analytics dashboard
- **AI Integration**: Personalized learning paths, content recommendations
- **Social Learning**: Peer interactions, study groups
- **Gamification**: Badges, leaderboards, achievements
- **Multi-tenancy**: Support for multiple institutions
- **Internationalization**: Full i18n/l10n support
- **Accessibility**: WCAG 2.1 AA compliance

### 6. Development Setup

#### Environment Configuration (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/modern_edx
REDIS_URL=redis://redis:6379/0

# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# AWS S3 (for media storage)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=modern-edx-media

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
```

#### Docker Compose Configuration
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: modern_edx
      POSTGRES_USER: edx_user
      POSTGRES_PASSWORD: edx_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  lms:
    build:
      context: .
      dockerfile: docker/lms/Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./services/lms:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://edx_user:edx_password@db:5432/modern_edx
      - REDIS_URL=redis://redis:6379/0

  cms:
    build:
      context: .
      dockerfile: docker/cms/Dockerfile
    command: python manage.py runserver 0.0.0.0:8001
    volumes:
      - ./services/cms:/app
    ports:
      - "8001:8001"
    depends_on:
      - db
      - redis

  celery:
    build:
      context: .
      dockerfile: docker/lms/Dockerfile
    command: celery -A lms worker -l info
    volumes:
      - ./services/lms:/app
    depends_on:
      - db
      - redis

  nginx:
    build:
      context: .
      dockerfile: docker/nginx/Dockerfile
    ports:
      - "80:80"
    depends_on:
      - lms
      - cms

volumes:
  postgres_data:
```

### 7. Migration Strategy
1. **Data Migration**: Create ETL scripts to migrate from MySQL to PostgreSQL
2. **API Compatibility Layer**: Maintain backward compatibility for existing integrations
3. **Gradual Migration**: Run legacy and modern systems in parallel during transition
4. **Feature Parity**: Ensure all critical features are available before full migration
5. **Testing Strategy**: Comprehensive test suite including unit, integration, and e2e tests

### 8. Commands to Run

```bash
# Initial setup
make setup

# Development
make dev

# Run tests
make test

# Build for production
make build

# Deploy
make deploy
```

### 9. Key Improvements Over Legacy
- **Performance**: 3-5x faster response times
- **Scalability**: Horizontal scaling with Kubernetes support
- **Maintainability**: Clean code architecture, comprehensive documentation
- **Security**: Modern security practices, regular dependency updates
- **Developer Experience**: Hot reloading, better debugging tools
- **User Experience**: Modern, responsive UI with better accessibility

### 10. Success Criteria
- All core LMS and CMS features working
- 90%+ test coverage
- Load handling: 10,000+ concurrent users
- Response time: <200ms for API calls
- Mobile-friendly responsive design
- Full API documentation
- Deployment automation with CI/CD

## Implementation Notes
- Start with core user authentication and course models
- Build API layer before frontend
- Use feature flags for gradual rollout
- Implement comprehensive logging and monitoring
- Create detailed migration guides for existing installations 
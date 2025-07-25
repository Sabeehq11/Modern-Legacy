# Modern edX Makefile

# Variables
DOCKER_COMPOSE_FILE = docker-compose.yml
DOCKER_COMPOSE_DEV_FILE = docker-compose.dev.yml
DOCKER_COMPOSE = docker-compose -f $(DOCKER_COMPOSE_FILE)
DOCKER_COMPOSE_DEV = docker-compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_DEV_FILE)

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

.PHONY: help setup dev build test clean logs restart migrate shell

# Default target
help:
	@echo "$(BLUE)Modern edX Platform Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@echo "  setup          - Initial setup for development"
	@echo "  build          - Build all Docker images"
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@echo "  dev            - Start development environment"
	@echo "  dev-build      - Build and start development environment"
	@echo "  stop           - Stop all services"
	@echo "  restart        - Restart all services"
	@echo "  logs           - Show logs from all services"
	@echo "  logs-lms       - Show LMS logs"
	@echo "  logs-cms       - Show CMS logs"
	@echo ""
	@echo "$(GREEN)Database Commands:$(NC)"
	@echo "  migrate        - Run database migrations"
	@echo "  migrate-lms    - Run LMS migrations only"
	@echo "  migrate-cms    - Run CMS migrations only"
	@echo "  shell          - Open Django shell"
	@echo "  shell-lms      - Open LMS Django shell"
	@echo "  shell-cms      - Open CMS Django shell"
	@echo "  superuser      - Create superuser for both LMS and CMS"
	@echo ""
	@echo "$(GREEN)Testing Commands:$(NC)"
	@echo "  test           - Run all tests"
	@echo "  test-lms       - Run LMS tests"
	@echo "  test-cms       - Run CMS tests"
	@echo "  coverage       - Run tests with coverage"
	@echo ""
	@echo "$(GREEN)Production Commands:$(NC)"
	@echo "  prod           - Start production environment"
	@echo "  prod-build     - Build and start production environment"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  clean-all      - Clean up everything including images"
	@echo "  requirements   - Update Python requirements"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code with black"

# Setup commands
setup:
	@echo "$(YELLOW)Setting up Modern edX development environment...$(NC)"
	@cp .env.example .env
	@echo "$(GREEN)Created .env file. Please update it with your settings.$(NC)"
	@$(DOCKER_COMPOSE) pull
	@$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Setup complete! Run 'make dev' to start development.$(NC)"

build:
	@echo "$(YELLOW)Building Docker images...$(NC)"
	@$(DOCKER_COMPOSE) build

# Development commands
dev:
	@echo "$(YELLOW)Starting development environment...$(NC)"
	@$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Development environment started!$(NC)"
	@echo "LMS: http://localhost:8000"
	@echo "CMS: http://localhost:8001"

dev-build:
	@echo "$(YELLOW)Building and starting development environment...$(NC)"
	@$(DOCKER_COMPOSE) up -d --build

stop:
	@echo "$(YELLOW)Stopping all services...$(NC)"
	@$(DOCKER_COMPOSE) down

restart:
	@echo "$(YELLOW)Restarting all services...$(NC)"
	@$(DOCKER_COMPOSE) restart

logs:
	@$(DOCKER_COMPOSE) logs -f

logs-lms:
	@$(DOCKER_COMPOSE) logs -f lms

logs-cms:
	@$(DOCKER_COMPOSE) logs -f cms

# Database commands
migrate:
	@echo "$(YELLOW)Running database migrations...$(NC)"
	@$(DOCKER_COMPOSE) exec lms python manage.py migrate
	@$(DOCKER_COMPOSE) exec cms python manage.py migrate

migrate-lms:
	@$(DOCKER_COMPOSE) exec lms python manage.py migrate

migrate-cms:
	@$(DOCKER_COMPOSE) exec cms python manage.py migrate

shell:
	@echo "$(YELLOW)Opening Django shell...$(NC)"
	@$(DOCKER_COMPOSE) exec lms python manage.py shell

shell-lms:
	@$(DOCKER_COMPOSE) exec lms python manage.py shell

shell-cms:
	@$(DOCKER_COMPOSE) exec cms python manage.py shell

superuser:
	@echo "$(YELLOW)Creating superuser for LMS...$(NC)"
	@$(DOCKER_COMPOSE) exec lms python manage.py createsuperuser
	@echo "$(YELLOW)Creating superuser for CMS...$(NC)"
	@$(DOCKER_COMPOSE) exec cms python manage.py createsuperuser

# Testing commands
test:
	@echo "$(YELLOW)Running all tests...$(NC)"
	@$(DOCKER_COMPOSE) exec lms python manage.py test
	@$(DOCKER_COMPOSE) exec cms python manage.py test

test-lms:
	@$(DOCKER_COMPOSE) exec lms python manage.py test

test-cms:
	@$(DOCKER_COMPOSE) exec cms python manage.py test

coverage:
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	@$(DOCKER_COMPOSE) exec lms coverage run --source='.' manage.py test
	@$(DOCKER_COMPOSE) exec lms coverage report
	@$(DOCKER_COMPOSE) exec cms coverage run --source='.' manage.py test
	@$(DOCKER_COMPOSE) exec cms coverage report

# Production commands
prod:
	@echo "$(YELLOW)Starting production environment...$(NC)"
	@$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d

prod-build:
	@echo "$(YELLOW)Building and starting production environment...$(NC)"
	@$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d --build

# Utility commands
clean:
	@echo "$(YELLOW)Cleaning up containers and volumes...$(NC)"
	@$(DOCKER_COMPOSE) down -v
	@docker container prune -f
	@docker volume prune -f

clean-all:
	@echo "$(RED)Cleaning up everything including images...$(NC)"
	@$(DOCKER_COMPOSE) down -v --rmi all
	@docker system prune -af

requirements:
	@echo "$(YELLOW)Updating Python requirements...$(NC)"
	@$(DOCKER_COMPOSE) exec lms pip freeze > services/lms/requirements.txt
	@$(DOCKER_COMPOSE) exec cms pip freeze > services/cms/requirements.txt

lint:
	@echo "$(YELLOW)Running code linting...$(NC)"
	@$(DOCKER_COMPOSE) exec lms flake8 .
	@$(DOCKER_COMPOSE) exec cms flake8 .

format:
	@echo "$(YELLOW)Formatting code with black...$(NC)"
	@$(DOCKER_COMPOSE) exec lms black .
	@$(DOCKER_COMPOSE) exec cms black .

# Health checks
health:
	@echo "$(YELLOW)Checking service health...$(NC)"
	@curl -f http://localhost:8000/health/ && echo "$(GREEN)LMS is healthy$(NC)" || echo "$(RED)LMS is unhealthy$(NC)"
	@curl -f http://localhost:8001/health/ && echo "$(GREEN)CMS is healthy$(NC)" || echo "$(RED)CMS is unhealthy$(NC)"

# Backup and restore
backup:
	@echo "$(YELLOW)Creating database backup...$(NC)"
	@$(DOCKER_COMPOSE) exec db pg_dump -U edx_user modern_edx > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore:
	@echo "$(YELLOW)Restoring database from backup...$(NC)"
	@read -p "Enter backup file path: " backup_file; \
	$(DOCKER_COMPOSE) exec -T db psql -U edx_user -d modern_edx < $$backup_file

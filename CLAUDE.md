# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Daily Dish application - a Django-based recipe management and ingredient purchase support system. The application provides both Web API (JWT auth) and External API (API Key auth) endpoints for recipe management, cooking history, and ingredient caching functionality.

## Common Development Commands

### Environment Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### Running the Application
```bash
# Development server
python manage.py runserver

# Production mode with ngrok
NGROK_MODE=true python manage.py runserver
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test daily_dish.tests
python manage.py test daily_dish.test_api

# Run specific test class
python manage.py test daily_dish.tests.UserModelTest
```

### Database Management
```bash
# Create superuser
python manage.py createsuperuser

# Check database state
python check_db_state.py

# Create API key
python create_api_key.py
```

## Development Workflow

This project follows a structured development approach with design documentation and task management:

- Requirements and design for each task must be documented in `.tmp/design.md`
- Detailed sub-tasks for each main task must be defined in `.tmp/task.md`
- Update `.tmp/task.md` as work progresses
- Create feature branches with `feature/` prefix
- Break tasks into small, manageable units for single commits
- Apply code formatter to maintain readability
- Ask for confirmation before committing changes

## Language and Documentation Rules

- **Think exclusively in English, but respond in Japanese**
- Documentation (JSDoc, Docstrings): **English**
- Code comments describing implementation background/reasoning: **Japanese**
- Comments for libraries like Vitest or zod-openapi: **English**
- Do not use emojis
- When writing Japanese, avoid unnecessary spaces (e.g., "Claude Code入門" not "Claude Code 入門")

## Development Tools

- Use Context7 MCP to retrieve latest library information
- Use Bash tool to find hidden folders like `.tmp`
- For concurrent independent processes, invoke tools concurrently, not sequentially

## Task Completion

- Send notification upon task completion using:
  ```bash
  osascript -e 'display notification "${TASK_DESCRIPTION} is complete" with title "${REPOSITORY_NAME}"'
  ```
- Notifications required even for minor tasks like formatting or refactoring

## Application Architecture

### Django Project Structure
- **Project**: `daily_dish_project/` - Main Django project configuration
- **App**: `daily_dish/` - Main application containing models, views, and APIs
- **Database**: SQLite3 (development), configurable for production
- **Authentication**: Dual system (JWT for web, API Key for external)

### Key Models
- **User**: Custom user model with email uniqueness
- **Recipe**: Unified recipe model (supports both existing and new recipes)
- **CookedDish**: Cooking history tracking
- **IngredientCache**: Temporary ingredient storage for cart functionality
- **ApiKey**: External API access management

### API Structure
- **Web API** (`/api/web/`): JWT authentication for web application
- **External API** (`/api/external/`): API Key authentication for external apps
- **Authentication Classes**: `HybridAuthentication`, `ApiKeyAuthentication`
- **Permission Classes**: `IsApiKeyAuthenticated`, `IsJWTAuthenticated`, `IsOwner`

### View Organization
- `views_web.py`: JWT-authenticated web application endpoints
- `views_external.py`: API Key-authenticated external application endpoints
- `views.py`: Base views (mostly unused)

### Special Features
- **Dual Authentication**: Single API supports both JWT and API Key auth
- **Ingredient Management**: Dynamic ingredient fields (1-20 per recipe)
- **Recipe Type Detection**: Automatic existing/new recipe classification via URL presence
- **NGROK Mode**: Production configuration for ngrok deployment

## Pull Request Format

When creating PRs, use this structure:
- **Title**: Brief summary of the task
- **Key Changes**: Describe changes and points of caution
- **Testing**: Specify which tests passed, which were added, and how to run tests
- **Related Tasks**: Provide links or numbers for related tasks
- **Other**: Include any special notes or relevant information
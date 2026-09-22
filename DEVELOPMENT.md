# Development Guide

## Environment Setup

### 1. Clone and Navigate to Project
```bash
cd "AI Customer Support Agent for Banking"
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


```bash

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

1. Set up your API keys in `.env` files when enabling hosted AI responses
2. Replace the in-process analytics store with the configured database for production
3. Add JWT-protected customer and analytics routes before production deployment
4. Add database migrations with Alembic
5. Commit code with meaningful messages
```
## Implemented Features
- Chat intent classification with MFA challenges and fraud escalation
- Customer lookup, balance, and transaction endpoints
- Live analytics summary, trend, and intent-category endpoints
- Streamlit customer lookup and analytics views connected to the backend
- Automated backend coverage for chat, security, and analytics behavior

## Running Locally

### Start Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd frontend
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run app.py
```

## Database Setup

For database migrations (when using SQLAlchemy):
```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend Tests (if applicable)
```bash
cd frontend
source venv/bin/activate
pytest tests/ -v
```

## Code Style and Linting

### Backend
```bash
cd backend
source venv/bin/activate
black app/ tests/
flake8 app/ tests/
isort app/ tests/
```

### Frontend
```bash
cd frontend
source venv/bin/activate
black . --exclude venv,.streamlit
flake8 . --exclude venv,.streamlit
isort . --skip-glob venv
```

## Docker Setup

Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Environment Variables

Copy `.env.example` to `.env` in both backend and frontend directories and update with your values:

### Backend (.env)
```
DATABASE_URL=sqlite:///./banking_support.db
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
DEBUG=True
```

### Frontend (.env)
```
BACKEND_URL=http://localhost:8000
API_TIMEOUT=30
DEBUG=True
```

## Debugging

### Backend Debug Mode
```bash
cd backend
source venv/bin/activate
python -m debugpy --listen 5678 -m uvicorn app.main:app --reload
```

### Frontend Debug Mode
```bash
cd frontend
source venv/bin/activate
streamlit run app.py --logger.level=debug
```

## Project Dependencies

### Backend (Core)
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- python-dotenv

### Frontend (Core)
- streamlit
- requests
- pandas
- plotly

## Common Issues

### Virtual Environment Not Activating
Ensure you're using the correct activation script for your OS.

### Port Already in Use
Change the port in the startup command:
```bash
# Backend on different port
python -m uvicorn app.main:app --reload --port 8001

# Frontend on different port
streamlit run app.py --server.port 8502
```

### Module Not Found Errors
Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

## Useful Commands

```bash
# Upgrade pip
pip install --upgrade pip

# List installed packages
pip list

# Generate requirements.txt (after adding new packages)
pip freeze > requirements.txt

# Check code style
black --check app/
```

## Next Steps

1. Set up your API keys in `.env` files
2. Configure database in `backend/app/config.py`
3. Start developing features in respective directories
4. Write tests as you develop
5. Commit code with meaningful messages

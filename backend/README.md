# Backend README

## Backend API

FastAPI-based backend for the AI Customer Support Agent.

### Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── dependencies.py      # Dependency injection
│   ├── routes/              # API endpoints
│   ├── models/              # Data models and database schemas
│   ├── services/            # Business logic
│   ├── database/            # Database setup and schemas
│   └── utils/               # Utility functions
├── tests/                   # Test suite
├── requirements.txt         # Dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

### Running the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run development server
python -m uvicorn app.main:app --reload

# Run on specific port
python -m uvicorn app.main:app --reload --port 8001
```

### API Documentation

Once running, view API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Environment Variables

Configure in `.env`:
```
DATABASE_URL=sqlite:///./banking_support.db
OPENAI_API_KEY=your_key_here
SECRET_KEY=your_secret_key
DEBUG=True
```

### API Endpoints

- `POST /api/v1/chat` - Send chat message
- `GET /api/v1/customers/{customer_id}` - Get customer info
- `POST /api/v1/customers` - Create customer
- `GET /api/v1/analytics` - Get analytics data

### Testing

```bash
pytest tests/ -v
pytest tests/ -v --cov=app
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

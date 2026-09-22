# Quick Start Guide - Running the AI Customer Support Agent

## Prerequisites
- Python 3.9 or higher
- pip or conda
- Git

## Installation & Setup

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to backend directory
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

# Create .env file
cp .env.example .env

# Optional: Add OpenAI API key to .env
# OPENAI_API_KEY=your_key_here
```

### 2. Frontend Setup (Terminal 2)

```bash
# Navigate to frontend directory
cd frontend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional, defaults to localhost)
cp .env.example .env
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
# Activate venv if not already
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Start Frontend (Terminal 2)

```bash
cd frontend
# Activate venv if not already
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start Streamlit app
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.
  
  Local URL: http://localhost:8501
```

## Usage

1. **Open Frontend**: Navigate to http://localhost:8501 in your browser
2. **Enter Customer ID** (optional): Use `CUST_001` or `CUST_002` for demo
3. **Chat with Agent**: Type your message and send

### Demo Queries to Try

```
- "What's my account balance?"
- "Show me my transactions"
- "I want to transfer $500"
- "I lost my card"
- "I think my account was hacked"
```

## API Documentation

**Backend API Docs**: http://localhost:8000/docs
- Interactive Swagger UI for all endpoints
- Test API endpoints directly
- View request/response schemas

## Architecture Overview

```
User Browser (Streamlit Frontend)
    ↓ (HTTP/REST)
FastAPI Backend Server
    ├─ Intent Classification (AI Service)
    ├─ Customer Service (Account Lookup)
    ├─ Auth Service (MFA, JWT)
    └─ Chat Router (Orchestration)
    ↓
Mock Database (Demo Data)
```

## Key Endpoints

### Chat
- **POST** `/api/v1/chat` - Send chat message

### Customer Info
- **GET** `/api/v1/customers/{customer_id}/info` - Get customer details
- **GET** `/api/v1/customers/{customer_id}/balance` - Get account balance
- **GET** `/api/v1/customers/{customer_id}/transactions` - Get transaction history

### Health
- **GET** `/health` - Backend health check
- **GET** `/` - API info

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
# On Windows:
netstat -ano | findstr :8000
# On macOS/Linux:
lsof -i :8000

# Kill process or use different port:
python -m uvicorn app.main:app --port 8001
```

### Frontend can't connect to backend
```
1. Verify backend is running on http://localhost:8000
2. Check BACKEND_URL in frontend/.env
3. Check CORS settings in backend/app/config.py
4. Firewall may be blocking traffic
```

### Streamlit rerun issues
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart app
# Press Ctrl+C and restart `streamlit run app.py`
```

### ModuleNotFoundError
```bash
# Ensure venv is activated and requirements installed
pip install -r requirements.txt --force-reinstall
```

## Development Workflow

### Adding a New Endpoint
1. Create route in `backend/app/routes/new_route.py`
2. Import in `backend/app/main.py`
3. Add to Swagger docs via docstring
4. Test at `/docs`

### Modifying Frontend
1. Edit component in `frontend/components/`
2. Streamlit auto-reloads on save
3. Check browser console for errors

### Running Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ -v --cov=app  # With coverage
```

## Configuration

### Backend (.env)
```
DATABASE_URL=sqlite:///./banking_support.db
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key
DEBUG=True
LOG_LEVEL=INFO
```

### Frontend (.env)
```
BACKEND_URL=http://localhost:8000
API_TIMEOUT=30
DEBUG=True
```

## Security Notes

⚠️ **Demo Only**: This is a demonstration/educational project with:
- Mock authentication (for demo purposes)
- No persistent database
- No real financial transactions
- Simplified security (use production-grade security in production)

**For Production**:
- Use proper OAuth2 + PKCE
- Enable database encryption
- Add rate limiting and WAF
- Implement proper audit logging
- Add comprehensive security testing

## Next Steps

1. Review [CASE_STUDY.md](../CASE_STUDY.md) for architecture details
2. Check [DEVELOPMENT.md](../DEVELOPMENT.md) for advanced setup
3. Explore API endpoints in Swagger UI
4. Examine code patterns in `backend/app/routes/chat.py`
5. Add your own custom intents to `backend/app/services/ai_service.py`

## Support

- **Documentation**: See README.md and DEVELOPMENT.md
- **Case Study**: See CASE_STUDY.md for detailed implementation guide
- **GitHub**: For issues and contributions

## License

Educational Use Only - See LICENSE file for details

---

**Happy Banking! 🏦**

*Last Updated: September 2024*

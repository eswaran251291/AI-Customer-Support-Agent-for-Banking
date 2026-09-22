# AI Customer Support Agent for Banking - Project Setup

## Project Overview
This is an AI-powered Customer Support Agent designed for banking institutions. It features a Python backend API and a Python-based frontend interface.

## Technology Stack
- **Backend**: Python with FastAPI or Flask
- **Frontend**: Python with Streamlit
- **Database**: SQLite/PostgreSQL
- **AI/ML**: OpenAI API, LangChain, or similar

## Project Structure
```
AI Customer Support Agent for Banking/
├── backend/                 # FastAPI/Flask backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── customers.py
│   │   │   └── analytics.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── customer.py
│   │   │   ├── conversation.py
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py
│   │   │   ├── customer_service.py
│   │   │   └── analytics_service.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── schemas.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py
│   │       └── helpers.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   ├── test_services.py
│   │   └── conftest.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/                # Streamlit frontend
│   ├── app.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── customer_info.py
│   │   ├── analytics.py
│   │   └── settings.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── chat_interface.py
│   │   └── customer_lookup.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   ├── styling.py
│   │   └── session_manager.py
│   ├── requirements.txt
│   ├── .streamlit/
│   │   └── config.toml
│   ├── .env.example
│   └── README.md
│
├── .github/
│   ├── copilot-instructions.md (this file)
│   └── workflows/
│       ├── backend-tests.yml
│       └── deploy.yml
│
├── docker-compose.yml
├── .env.example
├── README.md
└── DEVELOPMENT.md
```

## Key Features
- Real-time chat support with AI-powered responses
- Customer information lookup and management
- Conversation analytics and insights
- Multi-language support
- Secure authentication and authorization

## Development Workflow
1. Backend development in `backend/`
2. Frontend development in `frontend/`
3. Run both services locally using docker-compose or separate terminals
4. Write tests in respective `tests/` directories

## Getting Started
See DEVELOPMENT.md for detailed setup instructions.

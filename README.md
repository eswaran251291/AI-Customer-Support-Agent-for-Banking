# AI Customer Support Agent for Banking

An intelligent customer support system powered by AI for banking institutions. Built with Python using FastAPI for the backend and Streamlit for the frontend.

## Features

- **AI-Powered Chat**: Natural language processing for customer inquiries
- **Customer Management**: Lookup and manage customer information
- **Analytics Dashboard**: Real-time insights and analytics
- **Multi-channel Support**: Support for various communication channels
- **Secure Authentication**: Role-based access control and security

## Quick Start

### Prerequisites
- Python 3.9+
- pip or conda
- Virtual environment (recommended)

### Installation

1. Clone the repository
```bash
git clone <repo-url>
cd "AI Customer Support Agent for Banking"
```

2. Set up backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up frontend
```bash
cd ../frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:
```bash
cd frontend
source venv/bin/activate  # On Windows: venv\Scripts\activate
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`
The backend API will be available at `http://localhost:8000`

## Project Structure

See `.github/copilot-instructions.md` for detailed project structure and guidelines.

## Development

See `DEVELOPMENT.md` for development setup and guidelines.

## Documentation

- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
- [Development Guide](DEVELOPMENT.md)

## Contributing

Please follow the development guidelines in `DEVELOPMENT.md` when contributing.

## License

[Your License Here]

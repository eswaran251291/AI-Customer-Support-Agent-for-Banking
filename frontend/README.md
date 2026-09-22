# Frontend README

## Frontend Application

Streamlit-based frontend for the AI Customer Support Agent.

### Structure

```
frontend/
├── app.py                   # Main Streamlit app
├── pages/                   # Multi-page app pages
│   ├── __init__.py
│   ├── chat.py             # Chat interface
│   ├── customer_info.py    # Customer lookup
│   ├── analytics.py        # Analytics dashboard
│   └── settings.py         # Settings page
├── components/             # Reusable Streamlit components
│   ├── __init__.py
│   ├── sidebar.py          # Sidebar layout
│   ├── chat_interface.py   # Chat UI components
│   └── customer_lookup.py  # Customer search UI
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── api_client.py       # API communication
│   ├── styling.py          # Custom styling
│   └── session_manager.py  # Session state management
├── .streamlit/             # Streamlit config
│   └── config.toml        # Settings
├── .env.example           # Environment template
├── requirements.txt       # Dependencies
└── README.md             # This file
```

### Running the Frontend

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run application
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8502
```

### Accessing the Application

Open browser to: http://localhost:8501

### Pages

- **Chat**: Real-time conversation interface
- **Customer Info**: Look up customer information
- **Analytics**: View conversation analytics and metrics
- **Settings**: Configure application settings

### Environment Variables

Configure in `.env`:
```
BACKEND_URL=http://localhost:8000
API_TIMEOUT=30
DEBUG=True
```

### Configuration

Streamlit configuration in `.streamlit/config.toml`:
- Theme settings
- Page configuration
- Layout options

### Running Tests

```bash
pytest . -v
```

### Development Tips

1. Use `st.session_state` to persist data across reruns
2. Use `@st.cache_data` for caching expensive operations
3. Use `@st.cache_resource` for caching resources like API clients
4. Handle API errors gracefully with try/except and `st.error()`
5. Use columns and expanders for better layout organization

### Debugging

Enable debug mode in `.env`:
```
DEBUG=True
```

Then run:
```bash
streamlit run app.py --logger.level=debug
```

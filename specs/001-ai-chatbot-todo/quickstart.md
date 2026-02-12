# Quickstart Guide: Todo AI Chatbot with Natural Language Interface

## Overview
This guide provides instructions to quickly set up and run the Todo AI Chatbot system locally.

## Prerequisites
- Python 3.11+
- Node.js 18+
- Access to OpenAI API
- Access to Neon PostgreSQL database
- Better Auth account

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration:
# - OPENAI_API_KEY
# - DATABASE_URL (Neon PostgreSQL connection string)
# - BETTER_AUTH_SECRET
```

### 3. Database Setup
```bash
# With virtual environment activated
cd backend

# Run database migrations
alembic upgrade head

# Alternatively, initialize the database
python -c "from src.core.database import create_db_and_tables; create_db_and_tables()"
```

### 4. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local with your configuration:
# - BACKEND_URL (where backend is running)
# - NEXT_PUBLIC_BETTER_AUTH_URL
```

### 5. MCP Server Setup
```bash
# The MCP server is integrated into the backend
# Configuration is handled via environment variables
```

### 6. Run the Application

#### Option A: Separate Terminals
Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

#### Option B: Using Docker (if available)
```bash
docker-compose up --build
```

## API Endpoints
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API Documentation: `http://localhost:8000/docs`

## Testing the System
1. Visit `http://localhost:3000` in your browser
2. Sign in using the authentication system
3. Start interacting with the chatbot using natural language:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Complete task 1"
   - "Delete the meeting task"

## Troubleshooting
- If the backend doesn't start, verify your `.env` file has correct API keys
- If the frontend can't connect to the backend, check that both services are running and the URLs match
- If AI responses are slow, verify your OpenAI API key has sufficient quota

## Next Steps
- Explore the API documentation at `/docs`
- Review the data models in the `data-model.md` file
- Check the contract definitions in the `contracts/` directory
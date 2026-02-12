# Todo AI Chatbot Backend

This is the backend service for the Todo AI Chatbot with Natural Language Interface. It provides an API for managing todo tasks through natural language commands processed by an AI agent.

## Features

- Natural language processing for todo management
- AI-powered task operations (add, list, complete, delete, update)
- Conversation history and context management
- MCP (Model Context Protocol) tools for task operations
- Stateless architecture with database persistence

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLModel with PostgreSQL
- **AI Integration**: OpenAI Agents SDK (simulated)
- **Authentication**: Better Auth (simulated)

## API Endpoints

### Chat Endpoint
- `POST /api/v1/chat` - Process natural language input and return AI-generated response

### Task Management Endpoints
- `GET /api/v1/tasks` - Retrieve all tasks for the authenticated user
- `POST /api/v1/tasks` - Create a new task directly
- `PUT /api/v1/tasks/{task_id}` - Update an existing task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task
- `POST /api/v1/tasks/{task_id}/complete` - Mark a task as complete

### Conversation Endpoints
- `GET /api/v1/conversations/{conversation_id}/messages` - Retrieve messages for a specific conversation

## Environment Variables

- `DATABASE_URL` - PostgreSQL database connection string
- `OPENAI_API_KEY` - OpenAI API key (not used in this simulated implementation)
- `BETTER_AUTH_SECRET` - Better Auth secret (not used in this simulated implementation)

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run the application:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## Project Structure

```
backend/
├── src/
│   ├── models/           # SQLModel database models
│   ├── services/         # Business logic services
│   ├── mcp/              # MCP tools for task operations
│   ├── nlp/              # Natural language processing
│   ├── agents/           # AI agent implementation
│   ├── api/              # API route definitions
│   └── core/             # Core utilities (database, config, auth)
├── tests/                # Test files
└── requirements.txt      # Python dependencies
```

## Architecture

The backend follows a service-oriented architecture with clear separation of concerns:

- **Models**: Define the data structures using SQLModel
- **Services**: Contain business logic for task and conversation operations
- **MCP Tools**: Provide standardized interfaces for task operations
- **NLP Processor**: Handles natural language understanding
- **AI Agent**: Orchestrates the interaction between NLP and MCP tools
- **API Layer**: Exposes endpoints to the frontend
- **Core**: Contains shared utilities like database and configuration
# Todo AI Chatbot Frontend

This is the frontend for the Todo AI Chatbot with Natural Language Interface. It provides a chat interface for users to interact with the AI assistant to manage their todo tasks.

## Features

- Natural language chat interface for todo management
- Real-time interaction with AI assistant
- Visual feedback for task operations
- Responsive design for multiple devices

## Tech Stack

- **Framework**: React with Next.js
- **UI Components**: Custom built with CSS
- **API Client**: Fetch API for communication with backend

## Components

### ChatInterface
The main component that provides:
- Message display area
- User input field
- Loading indicators
- Task operation feedback
- Welcome message for new users

## API Integration

The frontend communicates with the backend through the ApiService which handles:
- Sending user messages to the chat endpoint
- Retrieving conversation history
- Fetching user tasks

## Environment Variables

- `BACKEND_URL` - The URL of the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Better Auth URL (not used in this implementation)

## Running the Application

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   │   └── chat/         # Chat interface components
│   ├── pages/            # Next.js pages
│   ├── services/         # API service clients
│   └── styles/           # CSS files
├── public/               # Static assets
├── package.json          # Node.js dependencies
└── README.md             # This file
```

## Usage

Once the application is running:

1. Navigate to the chat interface
2. Type natural language commands like:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Complete task 1"
   - "Delete the meeting task"
3. The AI assistant will process your commands and update your task list accordingly
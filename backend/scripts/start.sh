#!/bin/bash

# Backend startup script for the Todo Chatbot application

echo "Starting Todo Chatbot Backend..."

# Run database migrations if needed
# python -m alembic upgrade head

# Start the application with uvicorn
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
"""
Main API router for the Todo Chatbot application
"""
from fastapi import APIRouter
from . import todo, chat, health, metrics

api_router = APIRouter()

# Include routers for different modules
api_router.include_router(todo.router, prefix="/todos", tags=["todos"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
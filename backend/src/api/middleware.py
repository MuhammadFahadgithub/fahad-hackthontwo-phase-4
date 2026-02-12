"""
API routing and middleware for the Todo Chatbot application
"""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..utils import log_info, log_error

router = APIRouter()

# Middleware to log requests
async def log_requests_middleware(request: Request, call_next):
    log_info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    log_info(f"Response status: {response.status_code}")
    return response

# CORS middleware configuration
from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Rate limiting middleware (basic implementation)
from collections import defaultdict
import time

request_counts = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old requests (older than 1 minute)
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip] 
        if current_time - req_time < 60
    ]
    
    # Check if client has made more than 60 requests in the last minute
    if len(request_counts[client_ip]) >= 60:
        return JSONResponse(
            status_code=429,
            content={"message": "Rate limit exceeded"}
        )
    
    # Add current request
    request_counts[client_ip].append(current_time)
    
    response = await call_next(request)
    return response
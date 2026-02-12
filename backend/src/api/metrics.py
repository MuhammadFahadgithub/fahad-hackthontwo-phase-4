"""
Metrics endpoints for the Todo Chatbot application
"""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import time

router = APIRouter()

# Simple counter for API requests
request_count = 0
start_time = time.time()


@router.get("/metrics")
async def get_metrics():
    """
    Metrics endpoint for monitoring systems like Prometheus
    """
    global request_count
    request_count += 1
    
    # Calculate uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    
    # Generate Prometheus-style metrics
    metrics_text = f"""# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total {request_count}

# HELP uptime_seconds Application uptime in seconds
# TYPE uptime_seconds gauge
uptime_seconds {uptime_seconds}

# HELP app_info Application information
# TYPE app_info gauge
app_info{{version="1.0.0", name="todo-chatbot-backend"}} 1
"""
    
    return PlainTextResponse(content=metrics_text)
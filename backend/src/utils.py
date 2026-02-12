"""
Utility functions for error handling and logging
"""
import logging
from fastapi import HTTPException, status
from datetime import datetime
import json


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_info(message: str, extra_data: dict = None):
    """Log an info message with optional extra data"""
    if extra_data:
        logger.info(f"{message} | Extra data: {json.dumps(extra_data)}")
    else:
        logger.info(message)


def log_error(message: str, extra_data: dict = None):
    """Log an error message with optional extra data"""
    if extra_data:
        logger.error(f"{message} | Extra data: {json.dumps(extra_data)}")
    else:
        logger.error(message)


def log_warning(message: str, extra_data: dict = None):
    """Log a warning message with optional extra data"""
    if extra_data:
        logger.warning(f"{message} | Extra data: {json.dumps(extra_data)}")
    else:
        logger.warning(message)


def create_http_exception(status_code: int, detail: str):
    """Create an HTTP exception with the given status code and detail"""
    return HTTPException(
        status_code=status_code,
        detail=detail
    )


def handle_error(error: Exception, context: str = ""):
    """Handle an error by logging it and raising an HTTP exception"""
    error_msg = f"Error in {context}: {str(error)}"
    log_error(error_msg, {"exception_type": type(error).__name__})
    
    raise create_http_exception(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        f"An error occurred: {str(error)}"
    )
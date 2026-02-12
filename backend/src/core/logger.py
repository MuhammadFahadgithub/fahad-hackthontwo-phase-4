import logging
from datetime import datetime
from typing import Optional


class Logger:
    """
    Logging utility for the Todo AI Chatbot application
    """
    
    def __init__(self, name: str = "todo_ai_chatbot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create console handler if not already exists
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
    
    def log_info(self, message: str, user_id: Optional[str] = None, extra: Optional[dict] = None):
        """
        Log an info message
        """
        log_msg = f"[USER:{user_id or 'unknown'}] {message}"
        if extra:
            log_msg += f" | Extra: {extra}"
        self.logger.info(log_msg)
    
    def log_error(self, message: str, user_id: Optional[str] = None, error: Optional[Exception] = None, extra: Optional[dict] = None):
        """
        Log an error message
        """
        log_msg = f"[USER:{user_id or 'unknown'}] {message}"
        if error:
            log_msg += f" | Error: {str(error)}"
        if extra:
            log_msg += f" | Extra: {extra}"
        self.logger.error(log_msg)
    
    def log_warning(self, message: str, user_id: Optional[str] = None, extra: Optional[dict] = None):
        """
        Log a warning message
        """
        log_msg = f"[USER:{user_id or 'unknown'}] {message}"
        if extra:
            log_msg += f" | Extra: {extra}"
        self.logger.warning(log_msg)
    
    def log_debug(self, message: str, user_id: Optional[str] = None, extra: Optional[dict] = None):
        """
        Log a debug message
        """
        log_msg = f"[USER:{user_id or 'unknown'}] {message}"
        if extra:
            log_msg += f" | Extra: {extra}"
        self.logger.debug(log_msg)


# Global logger instance
app_logger = Logger()
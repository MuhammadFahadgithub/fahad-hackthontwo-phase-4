from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import HTTPException
from ..core.logger import app_logger
import traceback
import time


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling errors and logging requests
    """

    async def dispatch(self, request, call_next):
        start_time = time.time()

        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            # Log the HTTP exception
            app_logger.log_error(
                f"HTTP Exception: {e.detail}",
                extra={
                    "status_code": e.status_code,
                    "url": str(request.url),
                    "method": request.method
                }
            )
            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
            return response
        except Exception as e:
            # Log the unexpected exception
            app_logger.log_error(
                f"Unexpected error: {str(e)}",
                extra={
                    "url": str(request.url),
                    "method": request.method,
                    "traceback": traceback.format_exc()
                }
            )
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
            return response
        finally:
            # Log the request
            process_time = time.time() - start_time
            app_logger.log_info(
                f"Request completed",
                extra={
                    "url": str(request.url),
                    "method": request.method,
                    "process_time": f"{process_time:.4f}s"
                }
            )
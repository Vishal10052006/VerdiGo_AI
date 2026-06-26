import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Global middleware executed for every request.

    Responsibilities:
    - Log every request
    - Measure processing time
    - Add response timing header
    """

    async def dispatch(
        self,
        request: Request,
        call_next
    ):
        # Record start time
        start_time = time.perf_counter()

        # Log incoming request
        logger.info(
            "%s %s",
            request.method,
            request.url.path
        )

        # Continue request
        response = await call_next(request)

        # Calculate duration
        process_time = (
            time.perf_counter() - start_time
        )

        # Add debug header
        response.headers["X-Process-Time"] = (
            f"{process_time:.4f}"
        )

        # Log response
        logger.info(
            "%s %s -> %s (%.4fs)",
            request.method,
            request.url.path,
            response.status_code,
            process_time
        )

        return response
import threading

import django.utils.log
from django.http import HttpRequest, HttpResponse

from .wsgi import get_wsgi_application

local = threading.local()

__all__ = ["local", "get_wsgi_application"]


# Add content length to log records
def log_response_cor(
    message,
    *args,
    response: HttpResponse | None = None,
    request: HttpRequest | None = None,
    exception: Exception | None = None,
    logger=django.utils.log.request_logger,
    level=None,
) -> None:
    
    if getattr(response, "_has_been_logged", False):
        return

    if level is None:
        if response.status_code >= 500:
            level = "error"
        elif response.status_code >= 400:
            level = "warning"
        else:
            level = "info"

    if exception is not None:
        exc_info = (type(exception), exception, exception.__traceback__)
    else:
        exc_info = None

    getattr(logger, level)(
        message,
        *args,
        extra={
            "length": len(response.content) if hasattr(response, "content") else None,
            "status_code": response.status_code,
            "request": request,
        },
        exc_info=exc_info,
    )
    response._has_been_logged = True


# Patch log_response
django.utils.log.log_response = log_response_cor

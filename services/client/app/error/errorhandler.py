import logging
from starlette import status

from fastapi import Request, HTTPException

from entity import JSONResponseBuilder, Status

log = logging.getLogger(__name__)


def general_exception_error_handler(request: Request, exc: Exception):
    log.warning(f"Internal server error: {exc}")
    return JSONResponseBuilder() \
        .set_status_code(status.HTTP_500_INTERNAL_SERVER_ERROR) \
        .set_status(Status.failed) \
        .set_description(exc) \
        .build()


def http_exception_error_handler(request: Request, exc: Exception):
    log.warning(f"HTTP exception: {exc}")
    if not isinstance(exc, HTTPException):
        log.error(f"Incorrect exception type received: {type(exc)}: {str(exc)}")
        raise Exception(f"Incorrect exception type received: {type(exc)}")
    return JSONResponseBuilder() \
        .set_status_code(exc.status_code) \
        .set_status(Status.failed) \
        .set_description(exc.detail) \
        .build()

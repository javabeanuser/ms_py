import logging
from functools import wraps

from fastapi import HTTPException

log = logging.getLogger(__name__)


def database_error_handler(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        res = None
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            log.error(f"Cannot process with database query: {str(e)}")
            args[0].db.rollback()
            log.error(f"Rollback transaction")
            return res
    return wrap

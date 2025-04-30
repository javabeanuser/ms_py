import json

import uvicorn
from fastapi import Request, FastAPI, HTTPException, Depends
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from db import init_db
from db.services.registerservice import RegisterService
from db.session.session import get_session
from routers import client_router_v1
from routers import client_router_v2
from routers import util_router
from error import general_exception_error_handler, http_exception_error_handler

from config import Config


app = FastAPI()
log = logging.getLogger(__name__)

# V1
app.include_router(client_router_v1)

# V2
app.include_router(client_router_v2)

# Util
app.include_router(util_router)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_error_handler)
app.add_exception_handler(Exception, general_exception_error_handler)


@app.middleware("http")
async def catch_all_http(request: Request, call_next):
    # rs = await request.body()
    # j_body = json.loads(rs.decode())
    # subscriber_id = j_body['tracking_id']
    # message_id = j_body['request_id']
    # log.debug(f"Request: {request}")
    # db = await get_session().__anext__()
    # await RegisterService(db).create(subscriber_id=subscriber_id,
    #                                  message_id=message_id)
    response = await call_next(request)
    log.debug(f"Response: {response}")
    # await RegisterService(db).update(subscriber_id=subscriber_id,
    #                                  message_id=message_id)
    return response


@app.on_event("startup")
async def on_startup():
    log.info("Executing creating database")
    await init_db()


if __name__ == "__main__":
    uvicorn.run(app=app,
                host=Config.APP_HOST,
                port=Config.APP_PORT)

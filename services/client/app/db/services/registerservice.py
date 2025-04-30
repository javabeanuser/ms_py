from fastapi import HTTPException
from requests import Request
from sqlalchemy import select
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from util import JSONClientBuilder
from db import Client
from .abstractservice import ACRUDService
from starlette import status

from sqlalchemy import and_

import logging

from db.wrappers.database import database_error_handler
from ..entities.ormentities import RegisteringStatus, Registering

log = logging.getLogger(__name__)


class RegisterService(ACRUDService):
    def __init__(self, db):
        self.db: AsyncSession = db

    async def get(self, client: Client):
        raise NotImplemented

    @database_error_handler
    async def create(self, subscriber_id, message_id, status=RegisteringStatus.created):
        new_req = Registering(subscriber_id=subscriber_id,
                              message_id=message_id,
                              status=status)
        self.db.add(new_req)
        await self.db.commit()

    @database_error_handler
    async def update(self, subscriber_id, message_id, status=RegisteringStatus.processed):
        rs = await self.db.execute(select(Registering).where(
            and_(Registering.subscriber_id == int(subscriber_id),
                 Registering.message_id == int(message_id),)))
        db_message = rs.scalars().first()
        db_message.status = status
        if not db_message:
            log.error(f"Message with subscriber_id {subscriber_id}, message_id {message_id} is not found")
            return
        await self.db.commit()

    async def delete(self, client):
        raise NotImplemented

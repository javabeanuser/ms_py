from fastapi import HTTPException
from sqlalchemy import select, JSON
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from util import JSONClientBuilder
from .abstractservice import ACRUDService
from starlette import status

import logging

from db.wrappers.database import database_error_handler
from ..entities.ormentities import Client

log = logging.getLogger(__name__)


class ClientService(ACRUDService):
    def __init__(self, db):
        self.db: AsyncSession = db

    async def get(self, client: Client):
        clients = []
        rs = await self.db.execute(select(Client).where(
            or_(
                Client.id == client.id,
                Client.name.like(f"%{client.name}%"),
                Client.email.like(f"%{client.email}%"),
            )
        ))
        db_clients = rs.scalars().all()
        if not db_clients:
            raise HTTPException(status_code=404, detail="Client is not found")
        for db_client in db_clients:
            clients.append(JSONClientBuilder()
                           .id(db_client.id)
                           .name(db_client.name)
                           .email(db_client.email)
                           .build())
        return clients

    async def create(self, client: Client):
        clients = []
        new_client = Client(name=client['name'],
                            email=client['email'])
        self.db.add(new_client)
        await self.db.commit()
        await self.db.refresh(new_client)
        clients.append(JSONClientBuilder().id(new_client.id).name(new_client.name).email(new_client.email).build())
        return clients

    @database_error_handler
    async def update(self, client):
        rs = await self.db.execute(select(Client).where(Client.id == int(client.id)))
        db_client = rs.scalars().first()
        if not db_client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client is not found")

        log.debug(f"Update client.id = : {db_client.id}")

        is_updated = False
        if client.name and db_client.name != client.name:
            db_client.name = client.name
            is_updated = True
        if client.email and db_client.email != client.email:
            db_client.email = client.email
            is_updated = True
        if is_updated:
            await self.db.commit()
            await self.db.refresh(db_client)

        return [JSONClientBuilder().id(db_client.id).name(db_client.name).email(db_client.email).build()]

    @database_error_handler
    async def delete(self, client):
        rs = await self.db.execute(select(Client).where(Client.id == int(client.id)))
        db_client = rs.scalars().first()
        if db_client:
            log.debug(f"Update client.id = : {db_client.id}")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client is not found")
        await self.db.delete(db_client)
        await self.db.commit()

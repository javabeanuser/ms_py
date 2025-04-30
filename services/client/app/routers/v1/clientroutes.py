import logging

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi import APIRouter, Depends

from db.entities.ormentities import Client
from db.entities.pydentities import Client
from db.services.clientservice import ClientService
from entity.response import JSONResponseBuilder, Status
from db.session.session import get_session

log = logging.getLogger(__name__)

router = APIRouter(
    prefix=f"/api/v1/clients",
    tags=["Clients/v1"],
)


@router.get("/get")
async def get(id: int = None,
              name: str = None,
              email: str = None, db: AsyncSession = Depends(get_session)):
    if id is None and name is None and email is None:
        return JSONResponseBuilder() \
            .set_status_code(status.HTTP_404_NOT_FOUND) \
            .set_status(Status.failed) \
            .set_description("Client is not found") \
            .build()
    client = Client()
    client.id = id
    client.name = name
    client.email = email
    clients = await ClientService(db).get(client=client)
    log.debug(clients)
    return JSONResponseBuilder() \
        .set_status_code(status.HTTP_200_OK) \
        .set_status(Status.success) \
        .set_data(clients) \
        .build()


@router.post("/add")
async def add(client: Client, db: AsyncSession = Depends(get_session)):
    clients = await ClientService(db).create(client)
    return JSONResponseBuilder() \
        .set_status_code(status.HTTP_200_OK) \
        .set_status(Status.success) \
        .set_data(clients) \
        .build()


@router.patch("/update/{client_id}")
async def update(client_id: int, client: Client, db: AsyncSession = Depends(get_session)):
    client.id = client_id
    clients = await ClientService(db).update(client)
    return JSONResponseBuilder() \
        .set_status_code(status.HTTP_200_OK) \
        .set_status(Status.success) \
        .set_data(clients) \
        .build()


@router.delete("/delete/{client_id}")
async def delete(client_id: int, db: AsyncSession = Depends(get_session)):
    await ClientService(db).delete(client_id)
    return JSONResponseBuilder() \
        .set_status_code(status.HTTP_200_OK) \
        .set_status(Status.success) \
        .build()

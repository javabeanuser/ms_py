import logging

from fastapi import APIRouter
from starlette import status

from db.entities.pydentities import CDFRequest
from entity.response import JSONResponseBuilder, Status

log = logging.getLogger(__name__)

router = APIRouter(
    prefix=f"/api",
    tags=["Util"],
)


@router.get("/health-check")
async def health_check(payload: CDFRequest):
    tracking_id, subscriber_id, message_id = "default", "default", "default"

    if payload:
        tracking_id = payload.meta.tracking_id
        subscriber_id = payload.meta.subscriber_id
        message_id = payload.meta.message_id

    return JSONResponseBuilder() \
        .set_tracking_id(tracking_id) \
        .set_subscriber_id(subscriber_id) \
        .set_message_id(message_id) \
        .set_status_code(status.HTTP_200_OK) \
        .set_status(Status.success) \
        .set_description("The services are up is running") \
        .build()

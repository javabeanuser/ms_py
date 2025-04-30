import logging

from fastapi import APIRouter
from starlette import status

from entity.response import JSONResponseBuilder, Status

log = logging.getLogger(__name__)

router = APIRouter(
    prefix=f"/api",
    tags=["Util"],
)


@router.get("/health-check")
async def health_check():

    return JSONResponseBuilder() \
        .set_status_code(status.HTTP_200_OK) \
        .set_status(Status.success) \
        .set_description("The services up is running") \
        .build()

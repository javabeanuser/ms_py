import datetime
from typing import List

from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse


class Status:
    success = "success"
    failed = "failed"


class JSONResponseBuilder(BaseModel):
    status_code: int = status.HTTP_200_OK
    status: str = Status.success
    description: str = "Successfully Processed"
    tracking_id: str = 0
    subscriber_id: str = 0
    message_id: str = 0
    data: List[object] = []

    def __default(self, value, default_value=None):
        return value if value else default_value

    def set_tracking_id(self, tracking_id) -> "JSONResponseBuilder":
        self.tracking_id = tracking_id
        return self

    def set_subscriber_id(self, subscriber_id) -> "JSONResponseBuilder":
        self.subscriber_id = subscriber_id
        return self

    def set_message_id(self, message_id) -> "JSONResponseBuilder":
        self.message_id = message_id
        return self

    def set_status_code(self, status_code: int = 0) -> "JSONResponseBuilder":
        self.status_code = status_code
        return self

    def set_status(self, status: Status) -> "JSONResponseBuilder":
        self.status = str(status)
        return self

    def set_data(self, data_list: List[object]) -> "JSONResponseBuilder":
        self.data = data_list
        return self

    def set_description(self, description) -> "JSONResponseBuilder":
        self.description = str(description)
        return self

    def build(self) -> JSONResponse:
        json = {
            "meta": {
                "tracking_id": self.__default(self.tracking_id),
                "subscriber_id": self.__default(self.subscriber_id),
                "message_id": self.__default(self.message_id),
                "timestamp": str(datetime.datetime.now())
            },
            "status": {
                "status_code": self.__default(self.status_code),
                "status": self.__default(self.status),
                "description": self.__default(self.description)
            }
        }
        if self.data:
            json["data"] = self.__default(self.data)

        return JSONResponse(
            status_code=self.status_code,
            content=json
        )

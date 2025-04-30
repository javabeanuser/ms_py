from enum import Enum
from typing import Optional, List, Union, Text
from pydantic import BaseModel, Field


class BaseObj(BaseModel):
    id: Optional[int] = Field(default=None,
                              title="Entity database ID",
                              description="Optional id")


class Client(BaseObj):
    name: Optional[Text] = Field(None, description="Object name")
    email: Optional[Text] = Field(None, description="Object email", pattern=r"[A-z\.]+\@[A-z]+\.[A-z]+")


class RStatusEnum(str, Enum):
    SUCCESS = "open"
    FAILED = "in_progress"


class RMeta(BaseModel):
    tracking_id: Text = Field(default=None,
                              title="Tracking ID",
                              description="Unique identifier for tracking the message.")
    subscriber_id: Text = Field(default=None,
                                title="Subscriber ID",
                                description="Identifier for the subscribing service or entity.")
    message_id: Text = Field(default=None,
                             title="Message ID",
                             description="Unique identifier for the message.")


class RStatus(BaseModel):
    status_code: int = Field(default=200,
                             title="Response status code",
                             description="The code is equal HTTP response code")
    status: RStatusEnum = Field(default=None,
                                title="Response status",
                                description="Jus An enumeration entity success | failed")
    description: Text = Field(default=None,
                              title="Response description",
                              description="A description that app returns")


class CDFRequest(BaseModel):
    meta: RMeta = Field(default=None, title="Meta", description="Metadata about the message.")
    data: Optional[Union[List, Client]] = Field(None, description="Payload objects")


class CDFResponse(BaseModel):
    meta: RMeta = Field(default=None, title="Meta", description="Metadata about the message.")
    status: RStatus = Field(default=None, title="Status", description="RStatus type")
    data: Optional[Union[List, Client]] = Field(None, description="Payload objects")

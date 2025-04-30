from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from db.base import Base


@dataclass
class Client(Base):
    __tablename__ = "c_clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class Registering(Base):
    __tablename__ = "C_PROCESSED_MESSAGES"
    id = Column(Integer, primary_key=True)
    subscriber_id = Column(String)
    message_id = Column(String)
    status = Column(String)


class RegisteringStatus:
    created = "CREATED"
    processed = "PROCESSED"

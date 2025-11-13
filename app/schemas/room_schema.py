from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .user_schema import User


class Room(BaseModel):
    """
    Base class for a room schema.
    """

    pass


class CreateRoom(Room):
    """
    Schema used to create a chat room.
    """

    pass


class RoomMembers(BaseModel):
    """
    This schema represents response data for all group members.
    """

    member: str
    room: str


class RoomResponse(Room):
    """
    This schema that represents a response data for a chat room.
    """

    id: str
    host: User
    link: str
    password: str
    members: Optional[List[RoomMembers]] = []
    created_at: datetime

    class Config:
        from_attributes = True

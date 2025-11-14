from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .user_schema import User


class ChatRoom(BaseModel):
    """
    Base class for a room schema.
    """

    pass


class CreateRoom(ChatRoom):
    """
    Schema used to create a chat room.
    """

    pass


class RoomResponse(ChatRoom):
    """
    This schema that represents a response data for a chat room.
    """

    id: str
    host: User
    link: str
    password: str
    created_at: datetime

    class Config:
        from_attributes = True


class RoomMember(BaseModel):
    """
    This schema represent data for a single member in a chat room.
    """

    member: User

    class Config:
        from_attributes = True


class RoomMembers(BaseModel):
    """
    This schema represents response data for all members in a chat room.
    """

    member: str
    room: str



class JoinChatRoom(BaseModel):
    """
    Serialize request body when a user wants to join a room.
    """

    password: str

    class Config:
        from_attributes = True


class JoinChatRoomResponse(BaseModel):
    """
    This schema represents response data when a user joins a chat room.
    """

    room: RoomResponse
    members: List[RoomMember]

    class Config:
        from_attributes = True

from typing import Dict, List

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas import RoomResponse, User
from app.services import RoomService

router = APIRouter()


async def get_room_service() -> RoomService:
    return RoomService()


@router.get("/all-rooms", response_model=List[RoomResponse])
async def get_all_created_rooms(
    service: RoomService = Depends(get_room_service),
):
    """
    This endpoint retrieves all chat rooms.
    """
    return await service.get_all_rooms()


@router.get("/my-rooms", response_model=List[RoomResponse])
async def get_my_rooms(
    service: RoomService = Depends(get_room_service),
    user: User = Depends(get_current_user),
):
    """
    This endpoint retrieves all chat rooms created by the current user.
    """
    return await service.get_rooms_by_admin(user=user)


@router.get("/{room_link}/members", response_model=RoomResponse)
async def get_room_members(
    room_link: str,
    service: RoomService = Depends(get_room_service),
    user: User = Depends(get_current_user),
):
    """
    This endpoint retrieves all members of a specific chat room.
    """
    return await service.get_room_members(room_link=room_link)


@router.post("/create-room", response_model=RoomResponse)
async def create_room(
    service: RoomService = Depends(get_room_service),
    user: User = Depends(get_current_user),
):
    """
    This endpoint is used for creating a chat room.
    """
    return await service.create_room(user=user)


@router.post("/{room_link}/join-room", response_model=RoomResponse)
async def join_chat_room(
    room_link: str,
    service: RoomService = Depends(get_room_service),
    user: User = Depends(get_current_user),
):
    """
    This endpoint allows users to join a chat room.
    """
    return await service.join_room(room_link=room_link, user=user)


@router.delete("/{room_link}/leave-room", response_model=Dict[str, str])
async def leave_chat_room(
    room_link: str,
    service: RoomService = Depends(get_room_service),
    user: User = Depends(get_current_user),
):
    """
    This endpoint allows users to leave a chat room.
    """
    return await service.leave_room(room_link=room_link, user=user)


@router.delete("/{room_link}/delete-room", response_model=Dict[str, str], status=204)
async def delete_chat_room(
    room_link: str,
    service: RoomService = Depends(get_room_service),
    user: User = Depends(get_current_user),
):
    """
    This endpoint allows the host to delete a chat room.
    """
    return await service.delete_room(room_link=room_link, user=user)

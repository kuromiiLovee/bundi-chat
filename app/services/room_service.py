from typing import List

from app.core.exceptions import CannotDeleteRoomException, RoomDoesNotExistException
from app.models import Room, RoomMember
from app.schemas import CreateRoom, User


class RoomService:
    async def get_room(self, room_link: str) -> Room | None:
        """
        Get room by ID.
        """
        return await Room.filter(link=room_link)

    async def room_exists(self, room_link: str) -> bool:
        """
        Check if the room exists.
        """
        return await Room.filter(link=room_link).exists()

    async def get_rooms_by_admin(self, user: User) -> Room:
        """
        Retrieve all rooms created by the current user.
        """
        return await Room.filter(host=user).all()

    async def get_all_rooms(self) -> List[Room] | None:
        """
        Retrieve all rooms.
        """
        return await Room.all()

    async def create_room(self, user: User) -> Room:
        """
        Method used to create a chat room.
        """

        new_room = await Room.create(host=user)
        return new_room

    async def join_room(self, room_link: str, user: User):
        """
        Allow users with the room's link to join the chat room.
        """

        if not await self.room_exists(room_link):
            raise RoomDoesNotExistException()

        # create record for members who have joined the chat room.
        room = await self.get_room(room_link)

        members = await RoomMember.create(room=room, member=user.id)
        return members

    async def leave_room(self, room_link: str, user: User):
        """
        Allow users to leave a chat room.
        """

        if not await self.room_exists(room_link):
            raise RoomDoesNotExistException()

        room = await self.get_room(room_link)
        member_record = await RoomMember.filter(
            room=room,
            member=user.id,
        ).first()

        if member_record:
            await member_record.delete()

        return {"detail": "Successfully left the room."}

    async def get_room_members(self, room_link: str) -> List[User]:
        """
        Retrieve all members of a chat room.
        """

        if not await self.room_exists(room_link):
            raise RoomDoesNotExistException()

        room = await self.get_room(room_link)
        members = await RoomMember.filter(room=room).prefetch_related("member")
        return [member.member for member in members]

    async def delete_room(self, room_link: str, user: User):
        """
        Allow the host to delete a chat room.
        """

        if not await self.room_exists(room_link):
            raise RoomDoesNotExistException()

        room = await self.get_room(room_link)

        if room.host_id != user.id:
            raise CannotDeleteRoomException()

        await room.delete()
        return {"detail": "Room successfully deleted."}

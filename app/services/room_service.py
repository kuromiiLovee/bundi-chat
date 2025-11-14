from typing import List

from app.core.exceptions import (
    CannotDeleteRoomException,
    InvalidPasswordException,
    JoinChatRoomFailedException,
    RoomDoesNotExistException,
    UserIsBlockedFromJoiningRoomException,
)
from app.models import Room, RoomMember
from app.schemas import ChatRoom, JoinChatRoom, JoinChatRoomResponse, RoomResponse, User


class RoomService:
    async def get_room(self, room_link: str) -> Room | None:
        """
        Get room by ID.
        """
        return await Room.get_or_none(link=room_link).select_related("host")

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

    async def user_has_joined_room(self, room: ChatRoom, user: User) -> bool:
        """
        Check if a user has joined a specific chat room.
        """
        return await RoomMember.filter(room=room, member=user).exists()

    async def create_room(self, user: User) -> Room:
        """
        Method used to create a chat room.
        """

        new_room = await Room.create(host=user)
        return new_room

    async def join_room(
        self,
        room_link: str,
        user: User,
        entered_password: JoinChatRoom,
    ):
        """
        Allow users with the room's link to join the chat room.
        """

        room = await self.get_room(room_link)

        if not room:
            raise RoomDoesNotExistException()

        room_member = await RoomMember.filter(room=room, member=user).first()

        # check if user is blocked from joining a room
        if room_member and room_member.blocked:
            raise UserIsBlockedFromJoiningRoomException()

        # Verify password
        password = entered_password.model_dump()

        if room.password != password["password"]:
            if room_member:
                # Increment failed attempts
                room_member.failed_attempts += 1
                await room_member.save()

                # If more than 3 failed attempts, block the user
                if room_member.failed_attempts >= 3:
                    room_member.blocked = True
                    await room_member.save()

                raise JoinChatRoomFailedException(
                    failed_attempts=3
                    - (room_member.failed_attempts if room_member else 3)
                )

            raise InvalidPasswordException()

        # Reset failed attempts if password is correct
        if room_member:
            room_member.failed_attempts = 0
            await room_member.save()

        # add user if they haven't joined the chat room.
        member_exists = await self.user_has_joined_room(room, user)
        if not member_exists:
            await RoomMember.create(room=room, member=user)

        # Fetch all room members
        members = await RoomMember.filter(room=room).prefetch_related("member")

        # Map members to your RoomMember schema
        member_list = [
            {"member": User.from_orm(member.member).dict()} for member in members
        ]

        response = JoinChatRoomResponse(
            room=RoomResponse(
                id=str(room.id),
                host=User.from_orm(room.host),
                link=room.link,
                password=room.password,
                created_at=room.created_at,
            ).dict(),
            members=member_list,
        )

        return response

    async def leave_room(self, room_link: str, user: User):
        """
        Allow users to leave a chat room.
        """

        if not await self.room_exists(room_link):
            raise RoomDoesNotExistException()

        room = await self.get_room(room_link)
        member = await RoomMember.filter(room=room, member=user.id).first()

        if member:
            await member.delete()

        return {"detail": f"{user} left the room."}

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

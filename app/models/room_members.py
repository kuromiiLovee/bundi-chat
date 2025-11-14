from tortoise import fields
from tortoise.fields import OnDelete

from .base import BaseModel, TimestampMixin


class RoomMember(BaseModel, TimestampMixin):
    """
    This model represents members of a room.
    """

    room = fields.ForeignKeyField(
        "models.Room",
        on_delete=OnDelete.CASCADE,
        null=False,
        related_name="members",
    )
    member = fields.ForeignKeyField(
        "models.User",
        on_delete=OnDelete.NO_ACTION,
        null=False,
        related_name="room_members",
    )

    class Meta:
        ordering = ["member"]

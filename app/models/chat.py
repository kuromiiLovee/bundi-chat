from tortoise import fields
from tortoise.fields import OnDelete

from .base import BaseModel, TimestampMixin


class Chat(TimestampMixin, BaseModel):
    sender = fields.ForeignKeyField(
        "models.User",
        on_delete=OnDelete.CASCADE,
        related_name="sender",
        null=False,
    )
    room = fields.ForeignKeyField(
        "models.Room",
        on_delete=OnDelete.CASCADE,
        related_name="room_chats",
        null=False,
    )
    message = fields.TextField()

    class Meta:
        ordering = ["sender", "room"]

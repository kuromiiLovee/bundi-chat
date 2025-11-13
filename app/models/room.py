import random
import secrets

from tortoise import fields

from app.utils.room import hash_chat_room_password

from .base import BaseModel, TimestampMixin


class Room(TimestampMixin, BaseModel):
    link = fields.CharField(max_length=255, null=True, index=True)
    host = fields.ForeignKeyField(
        "models.User",
        on_delete=fields.CASCADE,
        related_name="room_admin",
        null=False,
    )
    password = fields.CharField(max_length=255)

    async def save(self, *args, **kwargs):
        # auto-generate link when creating a chat room
        if not self.link:
            self.link = secrets.token_urlsafe(16)

        # auto-generate password when creating a chat room
        if not self.password:
            # use token_urlsafe and room special characters to
            # create chat room password
            room_password = secrets.token_urlsafe(8) + str(
                random.sample(["!", "@", "#", "%", "^", "-", "_"], k=3)
            )
            self.password = hash_chat_room_password(room_password)

        await super().save(*args, **kwargs)

    class Meta:
        ordering = ["host", "link"]
        unique_together = ["host", "link"]

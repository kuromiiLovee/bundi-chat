import random
import secrets
import string

from tortoise import fields
from tortoise.fields import OnDelete

from .base import BaseModel, TimestampMixin


class Room(TimestampMixin, BaseModel):
    link = fields.CharField(max_length=255, null=True, index=True)
    host = fields.ForeignKeyField(
        "models.User",
        on_delete=OnDelete.CASCADE,
        related_name="room_admin",
        null=False,
    )
    password = fields.CharField(max_length=255)

    def generate_password(self, length=16, num_special_chars=3):
        """
        Generate a random password with letters, digits, and special characters.

        Args:
            length (int): Total length of the password (default is 12).
            num_special_chars (int): Number of special characters to include (default is 3).

        Returns:
            str: The generated password.
        """
        # Define character sets
        letters_and_digits = string.ascii_letters + string.digits
        special_characters = "!@#$%^&*-_+=<>?"

        # Generate the random part for the password (letters + digits)
        password_body = "".join(
            secrets.choice(letters_and_digits)
            for _ in range(length - num_special_chars)
        )

        # Select random special characters
        special_chars = "".join(
            secrets.choice(special_characters) for _ in range(num_special_chars)
        )

        # Combine the password body and special characters
        password_list = list(password_body + special_chars)

        # Shuffle the characters to mix the special characters
        random.shuffle(password_list)

        # Join the list back into a string
        password = "".join(password_list)

        return password

    async def save(self, *args, **kwargs):
        # auto-generate link when creating a chat room
        if not self.link:
            self.link = secrets.token_urlsafe(16)

        # auto-generate password when creating a chat room
        if not self.password:
            self.password = self.generate_password(num_special_chars=4)

        await super().save(*args, **kwargs)

    class Meta:
        ordering = ["host_id", "link"]
        unique_together = ["host_id", "link"]

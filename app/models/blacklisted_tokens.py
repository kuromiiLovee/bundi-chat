from datetime import datetime, timedelta, timezone

from tortoise import fields, models

from ..core.config import Config
from .base import TimestampMixin


class BlacklistedToken(TimestampMixin, models.Model):
    """
    Represents a JWT token that has been blacklisted and is no longer valid for authentication.

    Attributes:
        jti (str): The unique identifier (JWT ID) for the token, used as the primary key.
        expires_at (datetime): The UTC datetime when the blacklisted token expires.
    Methods:
        expiry_time(): Class method that returns the expiry time for a blacklisted token,
            calculated as the current UTC time plus the configured expiry duration.
    """

    id = fields.CharField(max_length=32, primary_key=True, editable=False)
    jti = fields.CharField(max_length=255, index=True)
    expires_at = fields.DatetimeField(null=False)

    class Meta:
        table = "blacklisted_tokens"

    @classmethod
    def expiry_time(cls):
        """
        Calculates the expiry time for a token based on the current UTC time and the configured expiry duration.

        Returns:
            datetime: The UTC datetime when the token will expire.
        """

        return datetime.now(timezone.utc) + timedelta(minutes=Config.JTI_EXPIRY)

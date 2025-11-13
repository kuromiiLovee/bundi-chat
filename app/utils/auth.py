import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from itsdangerous import URLSafeTimedSerializer
from jose import exceptions, jwt
from passlib.context import CryptContext

from ..core.config import Config
from ..models.blacklisted_tokens import BlacklistedToken

ALGORITHM = Config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRY = Config.ACCESS_TOKEN_EXPIRY
SECRET_KEY = Config.SECRET_KEY

serializer = URLSafeTimedSerializer(
    secret_key=Config.SECRET_KEY, salt="email-configuration"
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    """
    Hash a plain password using the configured password hashing context.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Verifies that a plain text password matches a hashed password.

    Args:
        plain_password (str): The plain text password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expiry: Optional[timedelta] = None,
    refresh: bool = False,
) -> str:
    """
    Generates a JSON Web Token (JWT) access token with the provided user data and expiry.

    Args:
        data (dict): The user data to include in the token payload.
        expiry (timedelta, optional): The duration until the token expires.
            If not provided, a default expiry (ACCESS_TOKEN_EXPIRY) is used.
        refresh (bool, optional): Indicates if the token is a refresh token. Defaults to False.

    Returns:
        str: The encoded JWT access token as a string.

    Notes:
        - The payload includes the user data, expiration time, a unique JWT ID (jti), and a refresh flag.
        - The token is signed using the secret and algorithm specified in the Config class.
    """

    # Initialize the payload dictionary
    payload = {}

    # Add user data, expiration, unique token ID, and refresh flag to the payload
    payload["user"] = data
    payload["exp"] = datetime.now(timezone.utc) + (
        expiry
        if expiry is not None
        else timedelta(
            seconds=ACCESS_TOKEN_EXPIRY,
        )
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    # Encode the payload into a JWT using the configured secret and algorithm
    token = jwt.encode(
        payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token  # Return the encoded JWT token as a string


def decode_access_token(token: str) -> dict | None:
    """
    Verifies and decodes a JWT access token.

    Args:
        token (str): The JWT access token to verify.

    Returns:
        dict: The decoded token data if verification is successful.
        None: If the token is invalid or verification fails.

    Raises:
        None: All exceptions are handled internally and logged.
    """

    try:
        token_data = jwt.decode(
            token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data

    except exceptions.JWTError as e:
        logging.exception(e)
        return None


def create_url_safe_token(data: dict):
    """
    Generates a URL-safe, serialized token from the provided data dictionary.

    Args:
        data (dict): The data to be serialized and encoded into the token.

    Returns:
        str: A URL-safe, serialized token representing the input data.
    """

    return serializer.dumps(data)


def decode_url_safe_token(private_key: str, max_age=300):
    """
    Decodes a URL-safe token using the provided private key.

    Args:
        private_key (str): The token to be decoded.
        max_age (int, optional): The maximum age (in seconds) the token is valid for.
        Defaults is 300.

    Returns:
        Any: The decoded data if the token is valid.

    Raises:
        Exception: Logs and suppresses any exception that occurs during decoding.
    """

    try:
        return serializer.loads(private_key, max_age=max_age)

    except Exception as e:
        logging.error(str(e))


async def add_token_to_blacklist(token_jti: str) -> None:
    """
    Adds a JWT token's JTI (unique identifier) to the blacklist in the database.
    This function creates a new BlacklistedToken entry with the provided token JTI and its expiry time,
    adds it to the database session, and commits the transaction. This is typically used to invalidate
    tokens (e.g., on logout) so they can no longer be used for authentication.

    Args:
        token_jti (str): The unique identifier (JTI) of the JWT token to blacklist.

    Returns:
        None
    """

    expires_at = BlacklistedToken.expiry_time()
    await BlacklistedToken.create(jti=token_jti, expires_at=expires_at)


async def token_in_blacklist(token_jti: str) -> bool:
    """
    Check if a given token's JTI (JWT ID) is present in the blacklist and has not expired.

    Args:
        token_jti (str): The unique identifier (JTI) of the token to check.

    Returns:
        bool: True if the token is found in the blacklist and has not expired, False otherwise.
    """

    result = await BlacklistedToken.filter(
        jti=token_jti, expires_at=datetime.now(timezone.utc)
    ).exists()

    return result  # return False if the token is not found, True otherwise

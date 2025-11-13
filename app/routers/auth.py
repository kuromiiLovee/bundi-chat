from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from ..core import exceptions
from ..core.config import Config
from ..core.dependencies import get_current_user
from ..core.token_bearer import AccessTokenBearer, RefreshTokenBearer
from ..schemas import (
    ConfirmResetPasswordSchema,
    CreatedUserResponse,
    CreateUser,
    LoginRequest,
    ResetPasswordSchema,
    UserResponse,
)
from ..services import AuthService
from ..utils.auth import (
    add_token_to_blacklist,
    create_access_token,
    create_url_safe_token,
    decode_url_safe_token,
    hash_password,
    verify_password,
)

router = APIRouter()

# service classes
auth_service = AuthService()

# time expiry of the refresh access token
REFRESH_TOKEN_EXPIRY = Config.REFRESH_TOKEN_EXPIRY


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_data: LoginRequest):
    """
    Authenticates a user and generates access and refresh tokens upon successful login.

    Args:
        user_data (LoginRequest): The login credentials provided by the user.
        db (AsyncSession, optional): The database session dependency.

    Raises:
        InvalidUserCredentialsException: If the user does not exist or the password is invalid.

    Returns:
        JSONResponse: A response containing a success message, access token, and refresh token.
    """

    data = user_data.model_dump()
    email = data["username"]
    password = data["password"]

    user = await auth_service.get_user(email)

    # check if the user exists before verifying user's password
    if user is None:
        raise exceptions.InvalidUserCredentialsException()

    password_valid = verify_password(password, user.password)

    if not password_valid:
        raise exceptions.InvalidUserCredentialsException()

    access_token = create_access_token(
        data={
            "username": user.username,
            "user_id": user.id,
        }
    )

    refresh_token = create_access_token(
        data={
            "username": user.username,
            "user_id": user.id,
        },
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
        refresh=True,
    )

    return JSONResponse(
        content={
            "message": "User logged in successfully!",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(
    bg_task: BackgroundTasks,
    user: CreateUser,
):
    """
    Creates a new user account and sends a verification email.

    Args:
        bg_task (BackgroundTasks): FastAPI background task manager for sending emails asynchronously.
        user (CreateUser): User registration data
        profile_image (UploadFile, optional): Optional profile image file uploaded by the user.
        db (AsyncSession): SQLAlchemy asynchronous database session dependency.

    Returns:
        JSONResponse: A response containing a success message and the created user's data if successful.
        status_code (int): HTTP status code indicating the result of the operation.
        201: Account created successfully.
        500: Internal server error if any error occurs during user creation or email sending.
        409: User with the provided email already exists.
        400: Invalid user credentials if the email is already taken or the password is invalid.
        403: User account not verified if the user tries to access a protected resource without verification.

    Raises:
        Exception: Rolls back the database transaction if any error occurs during user creation or email sending.
    """

    # Create an account for the user
    new_user = await auth_service.create_user_account(user)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Account created successfully! "
            "Check your email to verify your account.",
            "user": CreatedUserResponse.model_validate(new_user).model_dump(),
        },
    )


@router.get("/refresh-token")
async def refresh_token(token_data: dict = Depends(RefreshTokenBearer())):
    """
    Endpoint to refresh an access token using a valid refresh token.

    Args:
        token_data (dict): The decoded refresh token data, provided by the
        RefreshTokenBearer dependency.

    Returns:
        JSONResponse: A response containing a new access token and a success
        message if the refresh token is valid and not expired.

    Raises:
        InvalidTokenException: If the refresh token is invalid or expired.
    """

    expiry_timestamp = token_data["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            data={
                "email": token_data["user"]["username"],
                "user_id": token_data["user"]["id"],
            }
        )

        return JSONResponse(
            content={
                "message": "Access token refreshed successfully!",
                "access_token": new_access_token,
            }
        )

    raise exceptions.RefreshTokenRequiredException()


@router.get("/user/me", response_model=UserResponse)
async def get_user_details(user=Depends(get_current_user)):
    """
    Retrieve the details of the currently authenticated user. This endpoint returns the user object
    representing the currently authenticated user.

    Depends on:
        get_current_user: Dependency that provides the current authenticated user.

    Returns:
        The user object representing the currently authenticated user.
    """

    return user


@router.post("/reset-password")
async def reset_password(user_email: ResetPasswordSchema, bg_task: BackgroundTasks):
    """
    Handles password reset requests by generating a secure reset link and sending it to the user's email address.
    Args:
        user_email (ResetPasswordSchema): The schema containing the user's email address for password reset.
        bg_task (BackgroundTasks): FastAPI background task manager for sending the email asynchronously.
        user (User, optional): The currently authenticated user, injected via dependency.
    Returns:
        JSONResponse: A response indicating that the password reset instructions have been sent to the user's email.
    Raises:
        HTTPException: If the user is not authenticated or the email is invalid.
    Side Effects:
        Sends an email with a password reset link to the specified user.
    """

    email = user_email.email
    user = await auth_service.get_user(email)  # get user
    # join user's first name and last name separated by a space
    user_name = f"{user.first_name} {user.last_name}"
    private_key = create_url_safe_token({"email": email})
    reset_password_link = f"{
        Config.DOMAIN}/api/v1/auth/confirm-reset-password/{private_key}"

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password.",
        },
        status_code=200,
    )


@router.post("/confirm-reset-password/{user_private_key}")
async def confirm_reset_password(
    user_private_key: str,
    password: ConfirmResetPasswordSchema,
):
    """
    Resets the user's password after confirming the reset token and validating the new password.

    Args:
        user_private_key (str): The URL-safe token containing user identification (e.g., email).
        password (ConfirmResetPasswordSchema): Schema containing the new password and its confirmation.
        session (AsyncSession, optional): Database session dependency.

    Raises:
        PasswordIsShortException: If the new password is shorter than 8 characters.
        PasswordsDontMatchException: If the new password and confirmation do not match.
        UserNotFoundException: If no user is found with the provided email.

    Returns:
        JSONResponse: A response indicating whether the password reset was successful or if an error occurred.
    """

    new_password = password.new_password
    confirm_password = password.confirm_new_password

    if len(new_password) < 8:
        raise exceptions.PasswordIsShortException()

    if confirm_password != new_password:
        raise exceptions.PasswordsDontMatchException()

    user_data = decode_url_safe_token(user_private_key)
    user_email = user_data.get("email")

    if not user_email:
        return JSONResponse(
            content={
                "message": "Could not reset your password. An error ocurred!",
            },
            status_code=500,
        )

    # Check if user exists
    user = await auth_service.get_user(user_email)

    if not user:
        raise exceptions.UserNotFoundException()

    user_hashed_password = hash_password(new_password)
    await auth_service.update_user_profile(user, {"password": user_hashed_password})
    return JSONResponse(
        content={"message": "Your password was reset successfully!"},
        status_code=200,
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    """
    Logs out the current user by blacklisting their access token.
    This endpoint extracts the JWT ID (jti) from the provided access token,
    adds it to a blacklist to prevent further use, and returns a success message.

    Args:
        token_details (dict): A dictionary containing details of the access token,
            injected via dependency (AccessTokenBearer).

    Returns:
        JSONResponse: A response indicating successful logout.

    Raises:
        HTTPException: If token extraction or blacklisting fails.
    """

    jti = token_details["jti"]
    await add_token_to_blacklist(jti)
    return JSONResponse(
        content={
            "message": "User logged out successfully!",
        }
    )

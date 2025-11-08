from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import Config
from app.core.database import close_db, init_db
from app.middleware.auth import CustomAuthMiddleWare
from app.routers.auth import router as auth_router
from app.routers.chats import router as chat_router
from app.routers.rooms import router as room_router

# API version and docs URLs
api_version = "v1"
BASE_URL = f"/api/{api_version}"
WS_BASE_URL = f"/api/{api_version}"
swagger_docs_url = f"{BASE_URL}/docs"
redoc_docs_url = f"{BASE_URL}/redoc"


# startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup, initialize the database
    await init_db()

    # yield control to the application
    yield

    # on shutdown, close the db connection
    await close_db()


app = FastAPI(
    lifespan=lifespan,
    title="Chat API",
    description="",
    swagger_docs_url=swagger_docs_url,
    redoc_docs_url=redoc_docs_url,
    version="1.0.0",
)


# add middleware
app.add_middleware(CustomAuthMiddleWare)  # custom authentication middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# register routers
app.include_router(
    auth_router,
    prefix=f"{BASE_URL}/auth",
    tags=["Authentication"],
)
app.include_router(chat_router, prefix=f"{WS_BASE_URL}/chats", tags=["Chats"])
app.include_router(room_router, prefix=f"{BASE_URL}/rooms", tags=["Rooms"])

# register Tortoise ORM
register_tortoise(
    app,
    db_url=Config.DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

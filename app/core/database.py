from tortoise import Tortoise

from .config import Config

TORTOISE_ORM = {
    "connections": {
        "default": Config.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    """
    Initialize the database connection and generate schemas.
    This functions also enables Write-Ahead Logging (WAL) mode for SQLite.
    """
    await Tortoise.init(
        db_url=Config.DATABASE_URL,
        modules={"models": ["app.models"]},
    )
    # Enable WAL mode
    # conn = Tortoise.get_connection("default")
    # await conn.execute_script("PRAGMA journal_mode=WAL;")
    await Tortoise.generate_schemas()


async def close_db():
    """
    Close the database connection.
    """
    await Tortoise.close_connections()

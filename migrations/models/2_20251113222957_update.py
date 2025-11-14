from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "room" DROP CONSTRAINT IF EXISTS "uid_room_host_id_671034";
        ALTER TABLE "roommember" ADD "is_banned" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "roommember" ADD "failed_attempts" INT NOT NULL DEFAULT 0;
        ALTER TABLE "roommember" ADD "is_blocked" BOOL NOT NULL DEFAULT False;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_room_host_id_671034" ON "room" ("host_id", "link");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_room_host_id_671034";
        ALTER TABLE "roommember" DROP COLUMN "is_banned";
        ALTER TABLE "roommember" DROP COLUMN "failed_attempts";
        ALTER TABLE "roommember" DROP COLUMN "is_blocked";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_room_host_id_671034" ON "room" ("host_id", "link");"""


MODELS_STATE = (
    "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"
)

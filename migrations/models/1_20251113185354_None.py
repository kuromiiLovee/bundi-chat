from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "blacklisted_tokens" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" VARCHAR(32) NOT NULL PRIMARY KEY,
    "jti" VARCHAR(255) NOT NULL,
    "expires_at" TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_blacklisted_jti_20383b" ON "blacklisted_tokens" ("jti");
COMMENT ON COLUMN "blacklisted_tokens"."created_at" IS 'The date and time when the record was created';
COMMENT ON COLUMN "blacklisted_tokens"."updated_at" IS 'The date and time when the record was last updated';
COMMENT ON TABLE "blacklisted_tokens" IS 'Represents a JWT token that has been blacklisted and is no longer valid for authentication.';
CREATE TABLE IF NOT EXISTS "users" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" VARCHAR(32) NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True
);
CREATE INDEX IF NOT EXISTS "idx_users_usernam_266d85" ON "users" ("username");
COMMENT ON COLUMN "users"."created_at" IS 'The date and time when the record was created';
COMMENT ON COLUMN "users"."updated_at" IS 'The date and time when the record was last updated';
CREATE TABLE IF NOT EXISTS "room" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" VARCHAR(32) NOT NULL PRIMARY KEY,
    "link" VARCHAR(255),
    "password" VARCHAR(255) NOT NULL,
    "host_id" VARCHAR(32) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_room_host_id_671034" UNIQUE ("host_id", "link")
);
CREATE INDEX IF NOT EXISTS "idx_room_link_09bf43" ON "room" ("link");
COMMENT ON COLUMN "room"."created_at" IS 'The date and time when the record was created';
COMMENT ON COLUMN "room"."updated_at" IS 'The date and time when the record was last updated';
CREATE TABLE IF NOT EXISTS "chat" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" VARCHAR(32) NOT NULL PRIMARY KEY,
    "message" TEXT NOT NULL,
    "room_id" VARCHAR(32) NOT NULL REFERENCES "room" ("id") ON DELETE CASCADE,
    "sender_id" VARCHAR(32) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "chat"."created_at" IS 'The date and time when the record was created';
COMMENT ON COLUMN "chat"."updated_at" IS 'The date and time when the record was last updated';
CREATE TABLE IF NOT EXISTS "roommember" (
    "id" VARCHAR(32) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "member_id" VARCHAR(32) NOT NULL REFERENCES "users" ("id") ON DELETE NO ACTION,
    "room_id" VARCHAR(32) NOT NULL REFERENCES "room" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "roommember"."created_at" IS 'The date and time when the record was created';
COMMENT ON COLUMN "roommember"."updated_at" IS 'The date and time when the record was last updated';
COMMENT ON TABLE "roommember" IS 'This model represents members of a room.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)

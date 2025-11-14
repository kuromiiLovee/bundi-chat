from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "roommember" ALTER COLUMN "failed_attempts" SET DEFAULT 3;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "roommember" ALTER COLUMN "failed_attempts" SET DEFAULT 0;"""


MODELS_STATE = (
    "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"
)

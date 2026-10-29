import asyncio

from sqlalchemy import text

from database.session import engine
from database.models import Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # create_all never alters existing tables, so add columns introduced later
        await conn.execute(text("ALTER TABLE prediction_logs ADD COLUMN IF NOT EXISTS shap_values JSON"))

if __name__ == "__main__":
    asyncio.run(create_tables())
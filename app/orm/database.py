import asyncio
import logging
from config import async_engine
from orm.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_models():
    async with async_engine.begin() as conn:
        logger.info("Creating tables...")
        # Drop all tables (optional, for fresh start)
        # await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully")

if __name__ == "__main__":
    """If you desire, you can create the tables (models) inside the container running this"""
    asyncio.run(init_models())

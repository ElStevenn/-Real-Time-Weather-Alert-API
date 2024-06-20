from config import asyncSessionLocal, async_engine
from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

async def get_db() -> AsyncSession:
    """Get database session"""
    async with asyncSessionLocal() as db:
        yield db

async def register_new_user(user_body: schemas.UserCreateSchema):
    async with AsyncSession(async_engine) as session:
        async with session.begin():
            # Convert user_body to a dictionary
            new_user = models.User(**user_body.dict())
            session.add(new_user)
            await session.flush()
            
            # Get user id
            user_id = new_user.id
            return user_id

async def get_user(user_id: str):
    pass

async def main():
    user_schema = schemas.UserCreateSchema(
        username="your_username",  # Provide a username
        email="email@gmail.com",
        hashed_password="fake-hashed-password".encode('utf-8')
    )
    await register_new_user(user_schema)

if __name__ == "__main__":
    # Test Create new user
    asyncio.run(main())

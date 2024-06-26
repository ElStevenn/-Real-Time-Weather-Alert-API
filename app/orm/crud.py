from config import asyncSessionLocal, async_engine
from . import models, schemas
from ..security import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
# from ..security import get_password_hash
import asyncio

async def get_db() -> AsyncSession:
    """Get database session"""
    async with asyncSessionLocal() as db:
        yield db

async def register_new_user(username, email, hashed_password):
    async with AsyncSession(async_engine) as session:
        async with session.begin():
            new_user = models.User(username=username, email=email, hashed_password=hashed_password)
            session.add(new_user)
            await session.flush()

            user_id = new_user.id
            return user_id
        
async def get_user_profile(user_auth: str):
    pass

async def authenticate_user(user, password: str):

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

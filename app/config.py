import docker, os, asyncio
from docker.errors import NotFound
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__name__))
dockerClient = docker.from_env()
client = docker.APIClient(base_url='unix://var/run/docker.sock')

# DB Credentials
DEBUG = os.getenv('DEBUG_MODE', False)
SECRET_KEY = os.getenv('SECRET_KEY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

CSRF_ENABLED = True
CSRF_SESSION_KEY = SECRET_KEY
SQLALCHEMY_TRACK_MODIFICATIONS = False

try:
    client.start('db-container')
except NotFound:
    # Run Docker container 
    dockerClient.containers.run(
        'postgres:latest',
        name='db-container',
        environment=[
            'POSTGRES_PASSWORD=' + DB_PASS
        ],
        detach=True,
        ports={'5432/tcp': 5000},
        volumes={
            os.path.join(BASE_DIR, 'data'): {'bind': '/var/lib/postgresql/data'}
        }
    )

DB_HOST = client.inspect_container('db-container')['NetworkSettings']['Networks']['custom-isolated-network']['IPAddress']
print(DB_HOST)

async_engine = create_async_engine('postgresql+asyncpg://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST + ':5432/' + DB_NAME)
SQLALCHEMY_DATABASE_URI = 'postgresql+asyncpg://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST + ':5432/' + DB_NAME

asyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=True, 
    autoflush=False
)

async def get_all_db_names():
    """Sample function to show whether the function works or not"""
    async with async_engine.connect() as connection:
        result = await connection.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
        databases = [row[0] for row in result]
    return databases

async def main():
    res = await get_all_db_names()
    print(res)

if __name__ == "__main__":
    asyncio.run(main())

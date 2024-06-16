import docker
from docker.errors import NotFound
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


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
        name='container',
        environment=[
            'POSTGRES_PASSWORD=' + DB_PASS
        ],
        detach=True,
        ports={'5432/tcp': 5000},
        volumes={
            os.path.join(BASE_DIR, 'data'): {'bind': '/var/lib/postgresql/data'}
        }
    )

DB_HOST = client.inspect_container('some-postgres')['NetworkSettings']['Networks']['bridge']['Gateway']


engine = create_engine('postgresql+psycopg2://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST + ':5000/' + DB_NAME)
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST + ':5000/' + DB_NAME

Session = sessionmaker(bind=engine)

def get_all_db_names():
    """Sample function to show whether the function works or not"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
        databases = [row[0] for row in result]
    return databases

if __name__ == "__main__":
    print(get_all_db_names())
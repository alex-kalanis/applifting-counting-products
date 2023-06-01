import os
from dotenv import load_dotenv, dotenv_values
from .db import Db, Redis

load_dotenv()  # take environment variables from .env.

config = dotenv_values(".env")


def connect():
    Db.static().connect(
        user=os.environ['DB_USER'] if 'DB_USER' in os.environ else
        config['DB_USER'] if 'DB_USER' in config else 'dummy',
        pw=os.environ['DB_PASS'] if 'DB_PASS' in os.environ else
        config['DB_PASS'] if 'DB_PASS' in config else 'dummy',
        host=os.environ['DB_HOST'] if 'DB_HOST' in os.environ else
        config['DB_HOST'] if 'DB_HOST' in config else 'localhost',
        database=os.environ['DB_NAME'] if 'DB_NAME' in os.environ else
        config['DB_NAME'] if 'DB_NAME' in config else 'dummy'
    )

    Redis.static().connect(
        host=os.environ['REDIS_HOST'] if 'REDIS_HOST' in os.environ else
        config['REDIS_HOST'] if 'REDIS_HOST' in config else 'localhost',
        user=os.environ['REDIS_USER'] if 'REDIS_USER' in os.environ else
        config['REDIS_USER'] if 'REDIS_USER' in config else None,
        pw=os.environ['REDIS_PASS'] if 'REDIS_PASS' in os.environ else
        config['REDIS_PASS'] if 'REDIS_PASS' in config else None
    )


def uri_path() -> str:
    return Db.static().connect_uri(
        user=os.environ['DB_USER'] if 'DB_USER' in os.environ else
        config['DB_USER'] if 'DB_USER' in config else 'dummy',
        pw=os.environ['DB_PASS'] if 'DB_PASS' in os.environ else
        config['DB_PASS'] if 'DB_PASS' in config else 'dummy',
        host=os.environ['DB_HOST'] if 'DB_HOST' in os.environ else
        config['DB_HOST'] if 'DB_HOST' in config else 'localhost',
        database=os.environ['DB_NAME'] if 'DB_NAME' in os.environ else
        config['DB_NAME'] if 'DB_NAME' in config else 'dummy'
    )

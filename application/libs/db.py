import sqlalchemy as db
import redis as rd
from sqlalchemy.orm import scoped_session, sessionmaker
from .exceptions import CountingException


class Db:
    """
    Access database (Postgres)
    """

    instance = None

    @staticmethod
    def static():
        if not Db.instance:
            Db.instance = Db()
        return Db.instance

    def __init__(self):
        self.connection = None
        self.session = None

    def connect(self, user: str, pw: str, host: str, database: str):
        self.connection = db.create_engine(self.connect_uri(user, pw, host, database))
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.connection))

    def connect_uri(self, user: str, pw: str, host: str, database: str) -> str:
        return 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, pw, host, database)

    def get_connection(self):
        if not self.connection:
            raise CountingException('Connect to DB first!')
        return self.connection

    def get_session(self) -> scoped_session:
        if not self.session:
            raise CountingException('Connect to DB first!')
        return self.session


class Redis:
    """
    Access Redis
    """

    instance = None

    @staticmethod
    def static():
        if not Redis.instance:
            Redis.instance = Redis()
        return Redis.instance

    def __init__(self):
        self.connection = None

    def connect(self, host: str = 'localhost', user: str = None, pw: str = None):
        self.connection = rd.Redis(
            host=host,
            username=user,
            password=pw,
        )

    def get_connection(self):
        if not self.connection:
            raise CountingException('Connect to DB first!')
        return self.connection

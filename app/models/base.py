import sqlalchemy as sa
import sys, os
from sqlalchemy import orm
import dotenv

from operator import attrgetter
from inflection import pluralize, underscore
from flask_security.models import sqla

dotenv.load_dotenv(".flaskenv")
#engine = sa.create_engine("mysql://root:root@localhost:3306/flask_blog", echo=True)
engine = sa.create_engine(os.environ.get("FLASK_DATABASE_URL", "sqlite+pysqlite:///::memory::"), echo=True)

session = orm.scoped_session(
        orm.sessionmaker(bind=engine)
)

class Base(orm.DeclarativeBase):

    json_fields = []

    @orm.declared_attr
    def __tablename__(cls):
        return pluralize(underscore(cls.__name__))

    @orm.declared_attr
    def query(cls):
        return cls.session.query

    def save(self):
        session.add(self)
        session.commit()

    @orm.declared_attr
    def session(cls):
        return session

    def get_session(self):
        self.__class__.session.merge(self)
        return self.__class__.session

    def get_json(self, exclude=None):
        rtn = {}
        if exclude is None:
            exclude = []
        for name in self.json_fields:
            base_name = name.split(".")[0]
            if not base_name in exclude:
                getter = attrgetter(name)
                rtn[base_name] = getter(self)
        return rtn

sqla.FsModels.set_db_info(
        base_model=Base, 
        user_table_name='users', 
        role_table_name='roles',
        webauthn_table_name='web_authns',
)

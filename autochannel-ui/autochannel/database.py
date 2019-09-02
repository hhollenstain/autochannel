import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

LOG = logging.getLogger(__name__)
Base = declarative_base()

class AcDb:
    def __init__(self, app):
        self.app = app 

    def db_session(self):
        LOG.info(self.app.config['SQLALCHEMY_DATABASE_URI'])
        self.engine = create_engine(self.app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
        db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=self.engine))
        return db_session

    def create_database(self):
        from autochannel import models
        create = Base.metadata.create_all(bind=self.engine)
        print(create)
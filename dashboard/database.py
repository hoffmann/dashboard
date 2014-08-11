from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import g, current_app


def connect_db():
    import dashboard 
    return create_engine(dashboard.app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)#, echo=True) 

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db() 
    return db


def db_session():
    return scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=get_db()))
Base = declarative_base()

def init_db():
    import dashboard.models
    Base.metadata.create_all(bind=connect_db())


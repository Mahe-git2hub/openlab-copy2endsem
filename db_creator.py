from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import Index
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///namma_db.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Login(Base):
    __tablename__ = 'login'
    user_id = Column(Integer(), index=True, primary_key=True, autoincrement=True)
    name = Column(String(80))
    gender = Column(String(20))
    password = Column(String(40))
    email = Column(String(250))


# engine = create_engine('sqlite:///namma_db.db')
# Base.metadata.create_all(engine)

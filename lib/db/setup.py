# for database settings
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP

# to define tables and models
from sqlalchemy.ext.declarative import declarative_base

# sql settings
from sqlalchemy import create_engine

from lib import config

conf = config.JsonConfig('./config.json')
db_host = conf.value['db']['host']
db_name = conf.value['db']['db_name']
db_user = conf.value['db']['db_user']
db_pass = conf.value['db']['db_pass']

# declare declarative base
Base = declarative_base()


# User role table
class UserRole(Base):
    __tablename__ = 'user_role'
    role_id = Column(Integer, primary_key=True)
    role_code = Column(String(250), nullable=False)
    univer = Column(String(250), nullable=False)
    fak = Column(String(250))
    p_add_news = Column(Boolean)
    p_edit_news = Column(Boolean)


class UserAuth(Base):
    __tablename__ = 'user_auth'
    user_id = Column(Integer, primary_key=True)
    token = Column(String(250))


class UserSalt(Base):
    __tablename__ = 'user_salt'
    user_id = Column(Integer, primary_key=True)
    value = Column(String(250))


class UserLogin(Base):
    __tablename__ = 'user_login'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    role_id = Column(Integer, nullable=False)


class UserInfo(Base):
    __tablename__ = 'user_info'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    surname = Column(String(250), nullable=False)
    second_name = Column(String(250), nullable=True)
    course = Column(Integer, nullable=True)
    group = Column(String(250), nullable=True)
    subjects = Column(String(250), nullable=True)
    about = Column(String(250), nullable=True)
    profile_photo = Column(Integer, nullable=True)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    datetime = TIMESTAMP()
    head_photo = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)
    little_content = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)


# create engine instance
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}')

# create metadata for engine
Base.metadata.create_all(engine)

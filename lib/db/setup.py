# for database settings
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP

# to define tables and models
from sqlalchemy.ext.declarative import declarative_base

# sql settings
from sqlalchemy import create_engine

from lib import config

try:
    # normal config reading
    conf = config.JsonConfig('./config.json')
except:
    # config reading for tests
    conf = config.JsonConfig('../config.json')

db_host = conf.value['db']['host']
db_name = conf.value['db']['db_name']
db_user = conf.value['db']['db_user']
db_pass = conf.value['db']['db_pass']

# declare declarative base
Base = declarative_base()


class Faculty(Base):
    __tablename__ = 'faculty'
    faculty_id = Column(Integer, primary_key=True)
    value = Column(String(250))


class Univer(Base):
    __tablename__ = 'univer'
    univer_id = Column(Integer, primary_key=True)
    value = Column(String(250))


class UserRole(Base):
    __tablename__ = 'user_role'
    role_id = Column(Integer, primary_key=True)
    role_code = Column(String(250), nullable=False)
    faculty_id = Column(Integer)
    univer_id = Column(Integer)
    p_add_news = Column(Boolean)
    p_edit_news = Column(Boolean)


class UserAuth(Base):
    __tablename__ = 'user_auth'
    auth_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    token = Column(String(250))


class UserSalt(Base):
    __tablename__ = 'user_salt'
    salt_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    value = Column(String(250))


class UserLogin(Base):
    __tablename__ = 'user_login'
    login_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)


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
    role_id = Column(Integer, nullable=True)


class PushToken(Base):
    __tablename__ = 'push_token'
    token_id = Column(Integer, primary_key=True)
    token = Column(String(250), nullable=True)
    platform_service = Column(String(250), nullable=True)
    univer_id = Column(Integer, nullable=False)
    faculty_id = Column(Integer, nullable=False)
    state = Column(String(250), nullable=True)


class News(Base):
    __tablename__ = 'news'
    news_id = Column(Integer, primary_key=True)
    datetime = TIMESTAMP()
    head_photo = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)
    little_content = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)


class TokenPerm(Base):
    __tablename__ = 'token_perm'
    token = Column(String(250), nullable=False, primary_key=True)
    role_code = Column(String(250), nullable=False)
    univer = Column(String(250), nullable=False)
    faculty = Column(String(250), nullable=False)
    p_add_news = Column(Boolean, nullable=True)
    p_edit_news = Column(Boolean, nullable=True)


# create engine instance
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}')

# create metadata for engine
Base.metadata.create_all(engine)

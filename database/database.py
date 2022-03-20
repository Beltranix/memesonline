from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

import threading
import asyncio

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, UniqueConstraint, func


from config import Config


def start() -> scoped_session:
    engine = create_engine(Config.DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class Thumbnail(BASE):
    __tablename__ = "thumbnail"
    id = Column(Integer, primary_key=True)
    msg_id = Column(Integer)
    
    def __init__(self, id, msg_id):
        self.id = id
        self.msg_id = msg_id

Thumbnail.__table__.create(checkfirst=True)

async def df_thumb(id, msg_id):
    with INSERTION_LOCK:
        msg = SESSION.query(Thumbnail).get(id)
        if not msg:
            msg = Thumbnail(id, msg_id)
            SESSION.add(msg)
            SESSION.flush()
        else:
            SESSION.delete(msg)
            file = Thumbnail(id, msg_id)
            SESSION.add(file)
        SESSION.commit()

async def del_thumb(id):
    with INSERTION_LOCK:
        msg = SESSION.query(Thumbnail).get(id)
        SESSION.delete(msg)
        SESSION.commit()

async def get_thumb(id):
    try:
        t = SESSION.query(Thumbnail).get(id)
        y = await check(id)
        if y and y.value == 1:
            return t
        else:
            return None
    finally:
        SESSION.close()
def start() -> scoped_session:
    engine = create_engine(Config.DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class Users(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    
    def __init__(self, id):
        self.id = id
    
Users.__table__.create(checkfirst=True)

async def add_user(id, value):
    with INSERTION_LOCK:
        g = SESSION.query(Users).get(id)
        if not g:
            g = Users(id)
            SESSION.add(g)
            SESSION.flush()
        else:
            SESSION.delete(g)
            fil = Users(id)
            SESSION.add(fil)
        SESSION.commit()

async def remove_user(id):
    with INSERTION_LOCK:
        g = SESSION.query(Users).get(id)
        SESSION.delete(g)
        SESSION.commit()

async def check_user(id):
    try:
        y = SESSION.query(Users).get(id)
        if not y:
            return False
        else:
            return True
    finally:
        SESSION.close()


class Settings(BASE):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    
    def __init__(self, id, value):
        self.id = id
        self.value = value

Settings.__table__.create(checkfirst=True)

async def add(id, value):
    with INSERTION_LOCK:
        g = SESSION.query(Settings).get(id)
        if not g:
            g = Settings(id, value)
            SESSION.add(g)
            SESSION.flush()
        else:
            SESSION.delete(g)
            fil = Settings(id, value)
            SESSION.add(fil)
        SESSION.commit()

async def remove(id):
    with INSERTION_LOCK:
        g = SESSION.query(Settings).get(id)
        SESSION.delete(g)
        SESSION.commit()

async def check(id):
    try:
        y = SESSION.query(Settings).get(id)
        return y
    finally:
        SESSION.close()

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer, create_engine
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = 'sqlite:///' + os.path.join(BASE_DIR, 'kbot.db')

Base = declarative_base()
Session = sessionmaker()

engine = create_engine(connection_string, echo=True)

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    user = Column(String(1000), unique=True)
    user_lvl = Column(Integer)
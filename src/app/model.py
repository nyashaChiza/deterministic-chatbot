from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserState(Base):
    __tablename__ = "   states"

    id = Column(String, primary_key=True, index=True)
    state = Column(String)

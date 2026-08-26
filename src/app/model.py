from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserState(Base):
    __tablename__ = "UserState"

    id = Column(String, primary_key=True, index=True)
    state = Column(String)

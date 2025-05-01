import json
from sqlalchemy.orm import Session
from loguru import logger
from decouple import config
from .model import UserState, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod


DATABASE_URL = config("DATABASE_URL", default="sqlite:///./db.sqlite3")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


class BaseState(ABC):
    @abstractmethod
    def get_state(self, id: str) -> dict | None: ...
    @abstractmethod
    def set_state(self, id: str, state: dict) -> None: ...
    @abstractmethod
    def clear_state(self, id: str) -> None: ...
    @abstractmethod
    def clear_all(self) -> None: ...
    @abstractmethod
    def get_all(self) -> None: ...


class SQLAlchemyState(BaseState):
    def __init__(self):
        self.db = SessionLocal()

    def get_state(self, id: str) -> dict | None:
        record = self.db.query(UserState).filter(UserState.id == id).first()
        return json.loads(record.state) if record else None

    def set_state(self, id: str, state: dict) -> None:
        state = json.dumps(state)
        logger.warning(f"Setting state for {id}: {state}")
        record = self.db.query(UserState).filter(UserState.id == id).first()
        if record:
            record.state = state
        else:
            record = UserState(id=id, state=state)
            self.db.add(record)
        self.db.commit()

    def clear_state(self, id: str) -> None:
        self.db.query(UserState).filter(UserState.id == id).delete()
        self.db.commit()

    def clear_all(self) -> None:
        self.db.query(UserState).delete()
        self.db.commit()
    
    def get_all(self) -> dict:
        records = self.db.query(UserState).all()
        return {record.id: json.loads(record.state) for record in records if record.state}


class MemoryState(BaseState):
    def __init__(self):
        self._state = {}

    def get_state(self, user_id: str) -> dict | None:
        return self._state.get(user_id)

    def set_state(self, user_id: str, state: dict) -> None:
        self._state[user_id] = state

    def clear_state(self, user_id: str) -> None:
        self._state.pop(user_id, None)

    def clear_all(self) -> None:
        self._state = {}
    
    def get_all(self) -> dict:
        return self._state



# Singleton logic
_state_instance = None

def get_state_instance() -> BaseState:
    global _state_instance
    if _state_instance is None:
        backend = config("STATE_BACKEND", default="memory").lower()
        logger.info(f"Using {backend} state backend")
        if backend == "sqlite":
            _state_instance = SQLAlchemyState()
        else:
            _state_instance = MemoryState()
    return _state_instance

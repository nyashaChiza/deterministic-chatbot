from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.app.state import engine, get_state_instance, SQLAlchemyState

router = APIRouter(tags=["Health"])


@router.get("/health/")
def health_check():
    return {"status": "ok"}


@router.get("/readiness/")
def readiness_check():
    """
    health_check only confirms the process is up; this confirms the
    configured state backend is actually reachable - a real round trip for
    the sqlite backend, or a trivial check for the in-memory one (which has
    nothing external to fail).
    """
    state = get_state_instance()
    if not isinstance(state, SQLAlchemyState):
        return {"status": "ok", "checks": {"database": "not applicable (memory backend)"}}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        return JSONResponse(status_code=503, content={"status": "error", "checks": {"database": str(e)}})

    return {"status": "ok", "checks": {"database": "ok"}}

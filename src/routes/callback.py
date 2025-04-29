from fastapi import APIRouter, Request
from loguru import logger

router = APIRouter(prefix="/status-callback", tags=["Status Callback"])

@router.post("/")
async def status_callback(request: Request):
    data = await request.form()
    logger.info(f"Status Update: {data}")
    return {"status": "received"}
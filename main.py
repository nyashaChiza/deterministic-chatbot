
from typing import Union
from fastapi import FastAPI
from src.routes import webhook_router, callback_router

app = FastAPI(title='Deterministic-Chatbot', description='A deterministic-chatbot Backend', version='1.0.0') 

# Register routers
app.include_router(webhook_router)
app.include_router(callback_router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the Deterministic-Chatbot API"}


from typing import Union

from fastapi import FastAPI

app = FastAPI(title='Remittance Chatbot', description='Remittance Chatbot Backend', version='1.0.0') 


@app.get("/")
def read_root():
    return {"Hello": "World"}


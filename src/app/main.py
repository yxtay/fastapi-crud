from app.api import ping
from fastapi import FastAPI

app = FastAPI()


app.include_router(ping.router)

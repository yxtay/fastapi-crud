from fastapi import FastAPI

from app.api import notes, ping, tasks

app = FastAPI()


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

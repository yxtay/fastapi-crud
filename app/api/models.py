from typing import Any

from pydantic import BaseModel, Field, PositiveInt


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: PositiveInt


class TaskCreate(BaseModel):
    number: int


class TaskId(BaseModel):
    task_id: str


class TaskState(TaskId):
    state: str
    result: Any

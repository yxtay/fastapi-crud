from fastapi import APIRouter

from app.api.models import TaskCreate, TaskId, TaskState
from app.tasks import celery, fib_celery

router = APIRouter()


@router.post("/create", response_model=TaskId, status_code=200)
def task_create(task: TaskCreate):
    task = fib_celery.delay(task.number)

    result = {
        "task_id": task.id,
    }
    return result


@router.get("/state/{task_id}", response_model=TaskState, status_code=200)
def task_status(task_id: str):
    task = celery.AsyncResult(task_id)

    result = {
        "task_id": task.id,
        "state": task.state,
        "result": task.result,
    }
    return result

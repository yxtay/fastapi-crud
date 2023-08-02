from fastapi import APIRouter, status

from app.api.models import TaskCreate, TaskId, TaskState
from app.tasks import celery, fib_celery

router = APIRouter()


@router.post("/", response_model=TaskId, status_code=status.HTTP_200_OK)
def create_note(task: TaskCreate):
    task = fib_celery.delay(task.number)

    result = {
        "task_id": task.id,
    }
    return result


@router.get("/{task_id}", response_model=TaskState, status_code=status.HTTP_200_OK)
def get_task_status(task_id: str):
    task = celery.AsyncResult(task_id)

    result = {
        "task_id": task.id,
        "state": task.state,
        "result": task.result,
    }
    return result

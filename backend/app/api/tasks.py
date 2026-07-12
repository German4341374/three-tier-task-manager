from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import services
from app.database import get_db
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[TaskRead])
def read_tasks(db: DbSession) -> list[TaskRead]:
    return services.list_tasks(db)  # type: ignore[return-value]


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def add_task(data: TaskCreate, db: DbSession) -> TaskRead:
    return services.create_task(db, data)  # type: ignore[return-value]


@router.patch("/{task_id}", response_model=TaskRead)
def edit_task(task_id: int, data: TaskUpdate, db: DbSession) -> TaskRead:
    task = services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return services.update_task(db, task, data)  # type: ignore[return-value]


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int, db: DbSession) -> Response:
    task = services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    services.delete_task(db, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

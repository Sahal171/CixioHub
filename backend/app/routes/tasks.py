from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.task import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.auth.jwt_handler import get_current_user

router = APIRouter()

@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    new_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": new_task
    }

@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    tasks = db.query(Task).filter(
        Task.user_id == current_user.id
    ).all()

    return tasks

@router.get("/search")
def search_tasks(
    keyword: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
Task.user_id == current_user.id,
        Task.title.contains(keyword),
    ).all()
    return tasks

@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}")
def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.description = updated_task.description
    task.status = updated_task.status
    task.due_date = updated_task.due_date

    db.commit()
    db.refresh(task)

    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }
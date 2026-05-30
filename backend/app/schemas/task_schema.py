from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: str

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
    due_date: str
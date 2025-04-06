# ✅ app/schemas/task_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateTaskSchema(BaseModel):
    task_name: str
    description: str
    status: bool
    priority: str
    created_at: datetime
    assigned_user: str

class UpdateTaskSchema(BaseModel):
    task_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    priority: Optional[str] = None
    assigned_user: Optional[str] = None

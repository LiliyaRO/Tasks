from pydantic import BaseModel, Field
from typing import Optional, List

class TaskCreate(BaseModel):
    """Схема для создания новой задачи (POST-запрос)"""
    #id: int
    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    completed: bool = False

class TaskResponse(BaseModel):
    """Схема ответа с задачей"""
    id: int
    title: str
    completed: bool
    
    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    """Схема ответа со списком задач"""
    tasks: List[TaskResponse]
    total: int

class ErrorResponse(BaseModel):
    """Схема для ошибок"""
    detail: str
    error_code: int

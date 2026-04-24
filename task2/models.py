from pydantic import BaseModel, Field
from typing import Optional

class Task(BaseModel):
    """Модель задачи для хранения в JSON"""
    id: int
    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    completed: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Купить продукты",
                "completed": False
            }
        }

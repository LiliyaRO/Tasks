from fastapi import FastAPI, HTTPException, status
from models import Task
from schemas import TaskCreate, TaskResponse, TaskListResponse, ErrorResponse
from database import db
from starlette.responses import JSONResponse


# Создаём экземпляр FastAPI
app = FastAPI(
    title="Task Manager API",
    description="Простое API для управления задачами с JSON-базой данных",
    version="1.0.0"
)

@app.get("/", tags=["Info"])
async def root():
    """Информация об API"""
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "endpoints": {
            "GET /tasks": "Получить список всех задач",
            "POST /tasks": "Создать новую задачу",
            "DELETE /tasks/{task_id}": "Удалить задачу по ID"
        }
    }

@app.get("/tasks/", response_model=TaskListResponse, tags=["Задачи"])
async def get_tasks():
    """
    Вывести список всех задач.
    
    Returns:
        TaskListResponse: это объект со списком задач и их номером
    """
    tasks = db.get_all_tasks()
    return TaskListResponse(
        tasks=[TaskResponse(id=t.id, title=t.title, completed=t.completed) for t in tasks],
        total=len(tasks)
    )

@app.post("/tasks/", 
          response_model=TaskResponse, 
          status_code=status.HTTP_201_CREATED,
          tags=["Tasks"])
async def create_task(task: TaskCreate):
    """
    Создать новую задачу.
    
    Args:
        task (TaskCreate): здесь данные для новой задачи (title - обязательно, completed - опционально)
    
    Returns:
        TaskResponse: результат - созданная задача с присвоенным ID
    """
    new_task = db.add_task(title=task.title, completed=task.completed)
    return TaskResponse(id=new_task.id, title=new_task.title, completed=new_task.completed)

@app.delete("/tasks/{task_id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Tasks"])
async def delete_task(task_id: int):
    """
    Удалить задачу по её ID.
    
    Args:
        task_id (int): ID задачи для удаления
    
    Raises:
        HTTPException 404: выведет эту ошибку, если задача с указанным ID не найдена
    """
    success = db.delete_task(task_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    # Возвращаем None (204 No Content)
    return None

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Обработчик HTTP-исключений"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

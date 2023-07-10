from pydantic import BaseModel

class TodoItemCreate(BaseModel):
    title: str
    description: str

class TodoItemResponse(BaseModel):
    id: int
    title: str
    description: str

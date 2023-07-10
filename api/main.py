from fastapi import FastAPI
from routers import todo
from database import initialize_database


app = FastAPI()

app.include_router(todo.router)

initialize_database()
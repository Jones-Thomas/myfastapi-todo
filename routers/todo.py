import sqlite3
from fastapi import APIRouter, Depends
from typing import List
from schemas.todo import TodoItemCreate, TodoItemResponse
from models.todo import TodoItem

router = APIRouter()


def get_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        conn.close()


@router.post("/todos/", response_model=TodoItemResponse)
def create_todo_item(
        todo: TodoItemCreate, db: sqlite3.Cursor = Depends(get_db)
):
    cursor = db

    cursor.execute(
        """
        INSERT INTO todos (title, description)
        VALUES (?, ?)
        """,
        (todo.title, todo.description),
    )
    cursor.connection.commit()

    item_id = cursor.lastrowid

    todo_item = TodoItemResponse(
        id=item_id, title=todo.title, description=todo.description
    )

    return todo_item


@router.get("/todos/", response_model=List[TodoItemResponse])
def get_todo_items(db: sqlite3.Cursor = Depends(get_db)):
    cursor = db

    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()

    todo_items = []
    for todo in todos:
        todo_item = TodoItemResponse(
            id=todo[0], title=todo[1], description=todo[2]
        )
        todo_items.append(todo_item)

    return todo_items


@router.get("/todos/{item_id}", response_model=TodoItemResponse)
def get_todo_item(item_id: int, db: sqlite3.Cursor = Depends(get_db)):
    cursor = db

    cursor.execute("SELECT * FROM todos WHERE id=?", (item_id,))
    todo = cursor.fetchone()

    if todo:
        todo_item = TodoItemResponse(
            id=todo[0], title=todo[1], description=todo[2]
        )
        return todo_item
    else:
        return {"error": "TODO item not found"}


@router.put("/todos/{item_id}", response_model=TodoItemResponse)
def update_todo_item(
        item_id: int, todo: TodoItemCreate, db: sqlite3.Cursor = Depends(get_db)
):
    cursor = db

    cursor.execute(
        """
        UPDATE todos
        SET title=?, description=?
        WHERE id=?
        """,
        (todo.title, todo.description, item_id),
    )
    cursor.connection.commit()

    return TodoItemResponse(
        id=item_id, title=todo.title, description=todo.description
    )


@router.delete("/todos/{item_id}")
def delete_todo_item(item_id: int, db: sqlite3.Cursor = Depends(get_db)):
    cursor = db

    cursor.execute("DELETE FROM todos WHERE id=?", (item_id,))
    cursor.connection.commit()

    if cursor.rowcount > 0:
        return {"message": "TODO item deleted successfully"}
    else:
        return {"error": "TODO item not found"}

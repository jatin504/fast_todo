from fastapi import APIRouter, HTTPException
from models.todos import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()


# Get request method
@router.get("/")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos


@router.post("/")
async def post_todo(todo: Todo):
    collection_name.insert_one(dict(todo))


@router.put("/{id}")
async def update_todo(id: str, todo: Todo):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})


@router.delete("/delete/{todo_id}")
async def remove_todos(todo_id: str):
    result = collection_name.delete_one({"_id": ObjectId(todo_id)})

    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import asyncio

app = FastAPI()

class User(BaseModel):
    id: int
    name: str = Field(max_length=20)
    surname: str = Field(max_length=20)
    age: int = Field(ge=1)
    country: str = Field(max_length=20)

users = []

# Эндпоинт для получения всех пользователей
@app.get("/users", status_code=status.HTTP_200_OK)
async def get_users():
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

# Эндпоинт для получения пользователя по ID
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    for user in users:
        if user['id'] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Эндпоинт для создания нового пользователя
@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    users.append(user.dict())
    return user

# Эндпоинт для обновления пользователя
@app.patch("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: User):
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    for index, u in enumerate(users):
        if u['id'] == user_id:
            users[index] = user.dict()
            return {"message": "User updated"}
    raise HTTPException(status_code=404, detail="User not found")



# Эндпоинт для удаления пользователя
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    for index, u in enumerate(users):
        if u['id'] == user_id:
            del users[index]
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")


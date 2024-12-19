from fastapi import FastAPI
from app.routers import task, user


app = FastAPI()



@app.get('/')
async def welcome() -> dict:
    return {"message": "Welcom to Taskmaneger!"}

app.include_router(task.router)
app.include_router(user.router)
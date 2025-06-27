from fastapi import FastAPI
from .auth import router


app = FastAPI()

app.include_router(router.auth_router)


@app.get("/")
async def root():
    return {"message": "Welcome to weChat!"}

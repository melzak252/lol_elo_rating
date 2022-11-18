from fastapi import FastAPI
from app.lol_games import router as lol_games_router

app = FastAPI()

app.include_router(lol_games_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

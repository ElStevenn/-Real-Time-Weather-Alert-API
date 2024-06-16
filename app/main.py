from fastapi import FastAPI
from schemas import *
import asyncio
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"response": "Hello, welcome to Weather Real-Time Application"}

@app.post("/register", description="Register a new user")
async def register_new_user(request_boddy: RegisterUser):
    return {"response": "under construction"}


@app.post("/login", description="Login a user")
async def login_user(request_boddy: LoginUser):
    return {"response": "under construction"}

@app.post("/subscriptions", description="Subscription managment")
async def subscription_management():
    pass


async def main():
    config = uvicorn.Config("main:app", port=8080, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())

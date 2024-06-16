from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta, timezone
from schemas import *
from security import create_access_token, get_current_user
import asyncio
import uvicorn

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"response": "Hello, welcome to Weather Real-Time Application"}

@app.post("/register", description="Register a new user")
async def register_new_user(request_boddy: RegisterUser):
    return {"response": "under construction"}


@app.post("/login", description="Login a user")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
     # Authenticate user in db
    user = None 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
   

@app.get("/profile", description="Get user profile", response_model=Token)
async def get_profile(current_user: User = Depends(get_current_user)):
    return {"response": "under construction"}

"""Subscription Management"""
@app.post("/subscriptions", description="Subscription managment create")
async def subscription_create(current_user: User = Depends(get_current_user)):
    return {"response": "under construction"}

@app.get("/subscriptions", description="Subscription managment get")
async def subscription_get(current_user: User = Depends(get_current_user)):
    return {"response": "under construction"}

@app.delete("/subscriptions", description="Subscription managment delete")
async def subscription_delte(current_user: User = Depends(get_current_user)):
    return {"response": "under construction"}

"""Weather Data"""
@app.get("/weather/current", description="")
async def current_weather():
    {"response": "under construction"}

@app.get("/weather/forecast", description="")
async def weather_forecast():
    {"response": "under construction"}

"""Alerts"""
@app.post("/alerts", description="")
async def send_alert(current_user: User = Depends(get_current_user)):
    {"response": "under construction"}



async def main():
    config = uvicorn.Config("main:app", port=8080, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())

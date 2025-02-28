from fastapi import FastAPI
from app.routes import tickets, auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(tickets.router)

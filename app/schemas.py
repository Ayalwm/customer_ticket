from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models import TicketPriority, TicketStatus


from app.models import UserRole  
class TicketCreate(BaseModel):
    name: str
    email: EmailStr
    event_id: str
    title: str
    description: str
    priority: TicketPriority

class TicketResponse(TicketCreate):
    id: int
    status: TicketStatus

    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str 
    role: UserRole = UserRole.USER  
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole  

    class Config:
        orm_mode = True
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas, models, auth
from app.auth import get_current_user
from app.email_utils import send_ticket_update_email
from database import SessionLocal  

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/tickets", response_model=schemas.TicketResponse)
def create_ticket(ticket_data: schemas.TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(db, ticket_data)

@router.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = crud.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/tickets", response_model=list[schemas.TicketResponse])
def get_all_tickets(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends( auth.get_admin_user), 
):
    return crud.get_all_tickets(db) 
@router.get("/tickets/user/{email}", response_model=list[schemas.TicketResponse])
def get_tickets_by_user(email: str, db: Session = Depends(get_db)):
    return crud.get_tickets_by_user(db, email)


@router.patch("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
async def update_ticket_status(
    ticket_id: int, 
    status: models.TicketStatus, 
    db: Session = Depends(get_db), 
    admin_user: models.User = Depends(auth.get_admin_user)  
):
    updated_ticket = crud.update_ticket_status(db, ticket_id, status)
    
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    await send_ticket_update_email(updated_ticket)

    return updated_ticket
@router.get("/filtered_tickets", response_model=List[schemas.TicketResponse])
def get_tickets(
    status: Optional[schemas.TicketStatus] = Query(None),  # Use schema for enum validation
    priority: Optional[schemas.TicketPriority] = Query(None),  # Use schema for enum validation
    event_id: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    return crud.get_filtered_tickets(db, status, priority, event_id, start_date, end_date)

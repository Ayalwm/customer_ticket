from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app import models, schemas

def create_ticket(db: Session, ticket_data: schemas.TicketCreate):
    print(f"Received data: {ticket_data}")
    new_ticket = models.Ticket(
        name=ticket_data.name,
        email=ticket_data.email,
        event_id=ticket_data.event_id,
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority

    )
  
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def get_tickets_by_user(db: Session, email: str):
    return db.query(models.Ticket).filter(models.Ticket.email == email).all()

def get_all_tickets(db: Session):
    return db.query(models.Ticket).all()

def update_ticket_status(db: Session, ticket_id: int, new_status: models.TicketStatus):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if ticket:
        ticket.status = new_status
        db.commit()
        db.refresh(ticket)
    return ticket

def get_filtered_tickets(
    db: Session,
    status: Optional[models.TicketStatus] = None,
    priority: Optional[models.TicketPriority] = None,
    event_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    query = db.query(models.Ticket)

    if status:
        query = query.filter(models.Ticket.status == status)
    if priority:
        query = query.filter(models.Ticket.priority == priority)
    if event_id:
        query = query.filter(models.Ticket.event_id == event_id)
    if start_date:
        query = query.filter(models.Ticket.created_at >= start_date)
    if end_date:
        query = query.filter(models.Ticket.created_at <= end_date)

    tickets = query.all()
    return tickets
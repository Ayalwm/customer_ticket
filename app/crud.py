from sqlalchemy.orm import Session
from app import models, schemas

def create_ticket(db: Session, ticket_data: schemas.TicketCreate):
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

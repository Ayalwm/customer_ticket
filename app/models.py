from sqlalchemy import Column, Integer, String, Text, Enum
from database import Base
import enum

class TicketStatus(str, enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"

class TicketPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
 
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) 
    email = Column(String, nullable=False, index=True)  
    event_id = Column(String, nullable=False) 
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.LOW)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False) 
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

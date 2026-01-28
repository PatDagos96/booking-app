from sqlalchemy import Column, Integer, String
from database import Base

class Appointment(Base):
    __tablename__ = "appuntamenti"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String)
    servizio = Column(String)
    data = Column(String)  # Nuovo campo per gg/mm/aaaa
    ora = Column(String)   # Nuovo campo per hh:mm
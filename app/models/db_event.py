from sqlalchemy import Column, String, DateTime, JSON
from app.db import Base

class FHIRPatientEvent(Base):
    __tablename__ = "patient_events"

    id = Column(String, primary_key=True)  # Clave primaria única por evento
    encounter_id = Column(String)
    patient_id = Column(String)
    name = Column(String)
    birth_date = Column(String)
    gender = Column(String)
    timestamp = Column(DateTime(timezone=True))  # Para evitar errores con zonas horarias
    event_type = Column(String)
    data = Column(JSON)


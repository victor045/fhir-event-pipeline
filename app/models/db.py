from sqlalchemy import Column, String, DateTime, JSON
from app.db import Base

class PatientEventDB(Base):
    __tablename__ = "patient_events"

    patient_id = Column(String, primary_key=True)
    name = Column(String)
    birth_date = Column(String)
    gender = Column(String)
    encounter_id = Column(String)
    timestamp = Column(DateTime(timezone=True))  # 🛠 cambio aquí
    event_type = Column(String)
    data = Column(JSON)



import attr
from pydantic import BaseModel, Field


@attr.s(auto_attribs=True, frozen=True, slots=True)
class PatientEventAttrs:
    patient_id: str = attr.ib()
    name: str = attr.ib()
    birth_date: str = attr.ib()
    gender: str = attr.ib()
    encounter_id: str = attr.ib()
    timestamp: str = attr.ib()
    event_type: str = attr.ib()
    data: dict = attr.ib()


class PatientEvent(BaseModel):
    """
    Modelo de evento clínico tipo FHIR para ingestión de datos.
    """
    patient_id: str = Field(..., example="12345")
    name: str = Field(..., example="Juan Pérez")
    birth_date: str = Field(..., example="1980-01-01")
    gender: str = Field(..., example="male")
    encounter_id: str = Field(..., example="enc-56789")
    timestamp: str = Field(..., example="2025-07-12T08:30:00Z")
    event_type: str = Field(..., example="diagnosis")
    data: dict = Field(..., example={"code": "C34.1", "description": "Lung cancer"})

    class Config:
        extra = "forbid"

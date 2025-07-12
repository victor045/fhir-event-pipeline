#app/scripts/send_real_event.py
import asyncio
from app.models.fhir import PatientEvent
from app.services.kafka_producer import publish_event, close_producer

async def main():
    event = PatientEvent(
        patient_id="88888",
        name="Ana Gómez",
        birth_date="1992-07-12",
        gender="female",
        encounter_id="enc-89123",
        timestamp="2025-07-12T15:00:00Z",
        event_type="prescription",
        data={"medication": "Paracetamol", "dosage": "500mg"}
    )
    await publish_event(event)
    await close_producer()

if __name__ == "__main__":
    asyncio.run(main())


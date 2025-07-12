# test_publish.py
import asyncio
from app.models.fhir import PatientEvent
from app.services.kafka_producer import publish_event, close_producer
from app.config import get_settings


settings = get_settings()
print(f"📍 Conectando a: {settings.kafka_bootstrap_servers}")

async def main():
    print("📍 Conectando a:", get_settings().kafka_bootstrap_servers)
    event = PatientEvent(
        patient_id="12345",
        name="Juan Pérez",
        birth_date="1980-01-01",
        gender="male",
        encounter_id="enc-56789",
        timestamp="2025-07-12T08:30:00Z",
        event_type="diagnosis",
        data={"code": "C34.1", "description": "Lung cancer"}
    )
    await publish_event(event)
    await close_producer()

if __name__ == "__main__":
    asyncio.run(main())


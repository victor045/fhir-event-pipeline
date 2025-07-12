# app/services/kafka_consumer.py

import asyncio
import json
import uuid
from datetime import datetime

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app.config import get_settings
from app.utils.logging import logger
from app.models.fhir import PatientEvent
from app.models.db import PatientEventDB
from app.db import get_db

settings = get_settings()

async def start_consumer():
    consumer = AIOKafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id="fhir-consumer-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()
    logger.info("📥 Kafka consumer started and listening...")

    try:
        async for message in consumer:
            try:
                payload = json.loads(message.value.decode())
                logger.info(f"📩 Received event: {payload}")

                # Validar contra modelo FHIR
                event = PatientEvent(**payload)
                logger.info(f"✅ Event validated: {event.event_type} for patient {event.patient_id}")

                # Guardar en base de datos
                async for session in get_db():
                    new_event = PatientEventDB()
                    new_event.id = str(uuid.uuid4())
                    new_event.patient_id = event.patient_id
                    new_event.encounter_id = event.encounter_id
                    new_event.event_type = event.event_type
                    new_event.name = event.name
                    new_event.birth_date = event.birth_date
                    new_event.gender = event.gender
                    new_event.timestamp = datetime.fromisoformat(event.timestamp.replace("Z", "+00:00"))
                    new_event.data = event.data

                    session.add(new_event)
                    await session.commit()
                    logger.info("💾 Event saved to database")
                    break  # Importante para salir del generator

            except Exception as e:
                logger.warning(f"⚠️ Failed to process event: {e}")

    except KafkaError as e:
        logger.error(f"❌ Kafka consumer error: {e}")
    finally:
        await consumer.stop()
        logger.info("🛑 Kafka consumer stopped")

if __name__ == "__main__":
    asyncio.run(start_consumer())


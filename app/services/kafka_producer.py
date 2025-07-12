
import json
import os
import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from app.models.fhir import PatientEvent
from app.utils.logging import logger

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "fhir-events")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Inicializamos el productor Kafka
producer: AIOKafkaProducer = None

async def get_kafka_producer() -> AIOKafkaProducer:
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",  # garantizar exactly-once si se combina con idempotency
        )
        await producer.start()
        logger.info("✅ Kafka producer initialized")
    return producer

async def publish_event(event: PatientEvent):
    producer = await get_kafka_producer()

    try:
        value = event.dict()
        key = event.patient_id.encode("utf-8")  # particionado por paciente
        await producer.send_and_wait(KAFKA_TOPIC, key=key, value=value)
        logger.info(f"📤 Event published to Kafka: {value}")
    except KafkaError as e:
        logger.error(f"❌ Kafka publish failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"❌ Unexpected error publishing event: {e}")
        raise

async def close_producer():
    if producer:
        await producer.stop()
        logger.info("🛑 Kafka producer closed")


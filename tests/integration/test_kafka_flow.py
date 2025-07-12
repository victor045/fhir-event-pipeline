
import pytest
import asyncio
import json
from aiokafka import AIOKafkaConsumer
from httpx import AsyncClient
from app.main import app
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_kafka_event_flow():
    test_event = {
        "patient_id": "test123",
        "name": "Mario Gómez",
        "birth_date": "1985-11-10",
        "gender": "male",
        "encounter_id": "enc-99999",
        "timestamp": "2025-07-12T11:45:00Z",
        "event_type": "lab_result",
        "data": {"result": "positive", "type": "COVID-19"}
    }

    # Publicar el evento al endpoint FastAPI
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ingest", json=test_event)
    assert response.status_code == 200

    # Consumir desde Kafka
    consumer = AIOKafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id="test-consumer-group",
        auto_offset_reset="earliest",
        enable_auto_commit=False
    )

    await consumer.start()
    try:
        timeout = 10  # segundos
        end_time = asyncio.get_event_loop().time() + timeout
        found = False

        while asyncio.get_event_loop().time() < end_time:
            msg_batch = await consumer.getmany(timeout_ms=1000)
            for tp, messages in msg_batch.items():
                for message in messages:
                    payload = json.loads(message.value.decode())
                    if payload["patient_id"] == test_event["patient_id"]:
                        found = True
                        assert payload["data"] == test_event["data"]
                        break
                if found:
                    break
            if found:
                break

        assert found, "❌ No se encontró el evento en Kafka"
    finally:
        await consumer.stop()


import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app

@pytest.mark.asyncio
async def test_ingest_valid_event():
    payload = {
        "patient_id": "abc123",
        "name": "Jane Doe",
        "birth_date": "1990-06-12",
        "gender": "female",
        "encounter_id": "enc-12345",
        "timestamp": "2025-07-12T10:30:00Z",
        "event_type": "diagnosis",
        "data": {"code": "B20", "description": "HIV infection"}
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ingest", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_ingest_invalid_event():
    payload = {
        "patient_id": "abc123",
        "name": "Jane Doe"
        # falta el resto del schema
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ingest", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


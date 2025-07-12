
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

from app.models.fhir import PatientEvent
from app.services.kafka_producer import publish_event
from app.utils.logging import logger

from sqlalchemy.exc import SQLAlchemyError
from app.db import get_db
from app.models.db_event import FHIRPatientEvent
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

app = FastAPI(title="FHIR Event Pipeline", version="1.0.0")

# CORS config (útil si conectamos con frontend o dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cambiar a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 Response status: {response.status_code}")
    return response
    
@app.post("/ingest", response_model=dict, summary="Ingest patient FHIR-like event")
async def ingest_fhir_event(payload: PatientEvent, db: AsyncSession = Depends(get_db)):
    try:
        # 1. Publicar en Kafka
        await publish_event(payload)

        # 2. Guardar en base de datos
        db_event = FHIRPatientEvent(**payload.dict())
        db.add(db_event)
        await db.commit()

        return {"status": "ok", "message": "Event published and stored successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"❌ DB error: {e}")
        raise HTTPException(status_code=500, detail="DB error")
    except Exception as e:
        logger.error(f"❌ Error ingesting event: {e}")
        raise HTTPException(status_code=500, detail="Failed to process event")


@app.get("/health", summary="Check service health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


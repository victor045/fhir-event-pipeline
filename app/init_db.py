# app/init_db.py
from app.db import Base, engine
from app.models.db_event import FHIRPatientEvent

async def reset_db():
    async with engine.begin() as conn:
        print("📛 Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ Creating tables...")
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(reset_db())


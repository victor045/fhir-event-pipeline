import asyncio
from sqlalchemy import text
from app.db import engine

async def check_tables():
    async with engine.begin() as conn:
        result = await conn.run_sync(lambda sync_conn: sync_conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';")))
        tables = result.fetchall()
        print("🧾 Tablas en la base de datos:")
        for row in tables:
            print(" -", row[0])

if __name__ == "__main__":
    asyncio.run(check_tables())


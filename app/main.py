from fastapi import FastAPI
from app.db.database import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/health")
async def health_check():
    try: 
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return {"status": {"healthy"}}
    except Exception as e:
        return {"status" : "failed"}
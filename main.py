from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "shipping_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

@app.get("/user")
async def get_user():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        row = await conn.fetchrow("SELECT name FROM users LIMIT 1")
        await conn.close()
        if row:
            return {"name": row["name"]}
        return {"name": "Database Kosong (Isi dulu ya!)"}
    except Exception as e:
        logging.error(f"Error di /user: {e}")
        return {"name": f"Error Koneksi DB: {str(e)}"}
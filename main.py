from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import socket
import logging
import os

# Setup logging agar kita bisa lihat error di terminal
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gunakan alamat service 'mongodb' sesuai docker-compose
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

if MONGO_USER and MONGO_PASS:
    MONGO_DETAILS = f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongodb:27017/?authSource=admin"
else:
    # fallback: tanpa auth (misal saat testing lokal tanpa auth diaktifkan)
    MONGO_DETAILS = "mongodb://mongodb:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.shipping_db
collection = database.names_collection

@app.get("/get-name")
async def get_name():
    try:
        # Cek apakah database bisa diakses
        document = await collection.find_one({}, {"_id": 0, "name": 1})
        if document:
            return {"name": document["name"]}
        return {"name": "Database Kosong (Isi dulu ya!)"}
    except Exception as e:
        logging.error(f"Error di /get-name: {e}")
        return {"name": f"Error Koneksi DB: {str(e)}"}

@app.get("/get-container-id")
async def get_container_id():
    try:
        return {"container_id": socket.gethostname()}
    except Exception as e:
        return {"container_id": f"Error: {str(e)}"}
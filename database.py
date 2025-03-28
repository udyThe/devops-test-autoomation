from motor.motor_asyncio import AsyncIOMotorClient
import os

# Get MongoDB URI from environment variables or use default
DATABASE_URL = os.getenv("MONGO_URI", "mongodb+srv://minifighter8:Bn68J4fubIiKccsJ@cluster0.1p8jlij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = "fastapi_db"

client = AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]
collection = database["calculations"]

async def get_db():
    return database
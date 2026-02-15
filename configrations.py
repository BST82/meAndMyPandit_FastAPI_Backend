# configurations.py

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()  # loads .env

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["meAndMy"]

user_collection = db["userlogins"]
user_registration_collection = db["users"]
panchang_collection = db["monthly_panchang"]
festival_collection = db["festivals"]

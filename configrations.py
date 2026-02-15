from motor.motor_asyncio import AsyncIOMotorClient
import os
import certifi

MONGO_URI = os.getenv("MONGO_URI")

# Stop app if env missing (prevents localhost fallback)
if not MONGO_URI:
    raise Exception("MONGO_URI not set in environment")

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

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URI)

db = client["meAndMy"]          # Database name
user_collection = db["userlogins"]  # Collection name
user_registration_collection = db["users"]

# configurations.py

from motor.motor_asyncio import AsyncIOMotorClient

# ✅ MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://bt7355711982_db_user:BGo95wgi0pHSuLCt@meandmy.0vxnuac.mongodb.net/meAndMy?retryWrites=true&w=majority"

# Create client
client = AsyncIOMotorClient(MONGO_URI)

# Database
db = client["meAndMy"]

# Collections
user_collection = db["userlogins"]
user_registration_collection = db["users"]
panchang_collection = db["monthly_panchang"]
festival_collection = db["festivals"]   

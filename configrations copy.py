
import motor.motor_asyncio
import certifi
from motor.motor_asyncio import AsyncIOMotorClient



# uri = "mongodb+srv://bstudygroup19_db_user:moSnR74owYqCRmIT@meandmy.ftscjer.mongodb.net/?appName=meAndMy"
uri = "mongodb://localhost:27017/"

# MUST use AsyncIOMotorClient for FastAPI
# Get the path to the CA bundle provided by certifi
ca = certifi.where()

# Initialize the Async client with the TLS CA file
client = AsyncIOMotorClient(uri, tlsCAFile=certifi.where())     

# db = client.pandit_Db
db = client.meAndMy
user_collection = db["userlogins"]

# mongo db userid == bstudygroup19_db_user
# password == moSnR74owYqCRmIT

# mongodb+srv://bstudygroup19_db_user:moSnR74owYqCRmIT@meandmy.ftscjer.mongodb.net/?appName=meAndMy


# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://bstudygroup19_db_user:<db_password>@meandmy.ftscjer.mongodb.net/?appName=meAndMy"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
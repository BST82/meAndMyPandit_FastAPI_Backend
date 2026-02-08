from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserCreate
from configrations import user_registration_collection
from secure.secure import get_password_hash # Import hashing
import uuid

router = APIRouter()

ROLE_PRIORITY = {
    "Admin": 1, "Manager": 2, "Astrologer": 3, 
    "Pandit": 4, "Shopkeeper": 5, "User": 6
}

@router.post("/")
async def register_user(user_data: UserCreate):
    existing_user = await user_registration_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user_data.dict()
    
    # --- SECURITY: Hash the password ---
    user_dict["password"] = get_password_hash(user_data.password)
    user_dict["_id"] = str(uuid.uuid4())
    user_dict["priority"] = ROLE_PRIORITY.get(user_data.role.value, 6)

    await user_registration_collection.insert_one(user_dict)
    
    # Return user without the password field
    created_user = await user_registration_collection.find_one({"_id": user_dict["_id"]}, {"password": 0})
    return created_user
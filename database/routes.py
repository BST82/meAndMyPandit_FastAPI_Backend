from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from configrations import user_collection
from .models import user_helper
from .schemas import UserSchema, UpdateUserModel
from bson import ObjectId

router = APIRouter()

@router.post("/", response_description="Add new user")
async def create_user(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

@router.get("/", response_description="List all users")
async def get_users():
    users = []
    # In some Motor versions, you just iterate the cursor directly:
    cursor = user_collection.find()
    async for user in cursor:
        users.append(user_helper(user))
    return users
    
@router.get("/{id}", response_description="Get a single user")
async def get_user_data(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    if len(req) >= 1:
        update_result = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": req}
        )
        if update_result.modified_count == 1:
            updated_user = await user_collection.find_one({"_id": ObjectId(id)})
            return user_helper(updated_user)
    
    raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.delete("/{id}")
async def delete_user_data(id: str):
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User {id} not found")
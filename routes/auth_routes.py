from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWTError
from secure.secure import create_tokens, verify_password, SECRET_KEY, ALGORITHM
from configrations import user_registration_collection

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(payload: LoginRequest):
    # 1. Fetch user from MongoDB
    user = await user_registration_collection.find_one({"email": payload.email})
    
    # 2. Verify existence and password
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 3. Generate Tokens
    access_token, refresh_token = create_tokens({"sub": user["email"]})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.post("/refresh")
async def refresh_access_token(body: dict):
    refresh_token = body.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token missing")
        
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
            
        user_email = payload.get("sub")
        new_access, new_refresh = create_tokens({"sub": user_email})
        
        return {
            "access_token": new_access,
            "refresh_token": new_refresh
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import bcrypt

SECRET_KEY = "your_super_secret_key" 
ALGORITHM = "HS256"

# Setup Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt directly to bypass Python 3.14 passlib bugs.
    """
    # 1. Convert string to bytes
    password_bytes = password.encode('utf-8')
    
    # 2. Generate salt and hash (bcrypt handles the 72-byte limit internally)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # 3. Return as string for MongoDB storage
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def create_tokens(data: dict):
    # Access Token
    access_expire = datetime.utcnow() + timedelta(minutes=15)
    access_token = jwt.encode({**data, "exp": access_expire, "type": "access"}, SECRET_KEY, algorithm=ALGORITHM)
    
    # Refresh Token
    refresh_expire = datetime.utcnow() + timedelta(minutes=30)
    refresh_token = jwt.encode({**data, "exp": refresh_expire, "type": "refresh"}, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token, refresh_token
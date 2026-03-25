from datetime import datetime, timedelta
from typing import Any, Dict
import os

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

# ---------------- LOAD ENV VARIABLES ----------------
load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecret")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# ---------------- PASSWORD HASHING ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- OAUTH2 ----------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------------- UTILITY FUNCTIONS ----------------

def hash_password(password: str) -> str:
    """
    Hash a password (up to 72 chars for bcrypt)
    """
    return pwd_context.hash(password[:72])

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a password against its hash
    """
    return pwd_context.verify(plain[:72], hashed)

def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create JWT token with expiration
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------- CURRENT USER ----------------

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """
    Decode JWT token and return user info
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- ADMIN CHECK ----------------

def require_admin(user: Dict[str, str] = Depends(get_current_user)) -> Dict[str, str]:
    """
    Dependency to enforce admin-only access
    """
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
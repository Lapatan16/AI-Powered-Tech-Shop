import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Any
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("JWT_ALGORITHM")
EXPIRE = os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

def generate_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=float(EXPIRE))

    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
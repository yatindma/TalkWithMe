import datetime

import paseto
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from paseto.keys.asymmetric_key import AsymmetricSecretKey
from paseto.protocols.v4 import ProtocolVersion4

from mongodb_helper import get_users_collection

# Generate a new AsymmetricSecretKey for signing PASETO tokens
SECRET_KEY = AsymmetricSecretKey.generate(protocol=ProtocolVersion4)

# PASETO configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Define an OAuth2 password bearer scheme with a custom token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    now = datetime.datetime.utcnow()
    expire = now + (expires_delta or datetime.timedelta(minutes=15))
    to_encode.update({"exp": expire.timestamp()})

    return paseto.create(
        key=SECRET_KEY,
        purpose='public',
        claims={'my claims': to_encode},
        exp_seconds=300
    )


async def get_current_user(token: str = Depends(oauth2_scheme), users_col=Depends(get_users_collection)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = paseto.parse(
            key=SECRET_KEY,
            purpose='public',
            token=token,
        )

        user_id = payload['message']['my claims'].get('user_id')

        if user_id is None:
            raise paseto.PasetoValidationError("Token does not contain a user ID")
    except ValueError:
        raise paseto.PasetoValidationError("Invalid token")

    user = users_col.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return {"user_id": user_id}

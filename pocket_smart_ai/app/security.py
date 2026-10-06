from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from fastapi import HTTPException
from fastapi import status

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from .config import settings


password_hash = PasswordHash(
    (
        Argon2Hasher(),
    )
)


bearer_scheme = HTTPBearer(
    auto_error=False
)


ALGORITHM = "HS256"


def hash_password(password: str) -> str:

    return password_hash.hash(
        password
    )


def verify_password(
    password: str,
    hashed: str
) -> bool:

    return password_hash.verify(
        password,
        hashed
    )


def create_access_token(
    user_id: int
) -> str:

    expires = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_minutes
        )
    )

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expires
        },
        settings.secret_key,
        algorithm=ALGORITHM
    )


def get_user_id_from_token(
    credentials: HTTPAuthorizationCredentials | None
) -> int:

    if not credentials:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    try:

        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )

        return int(
            payload["sub"]
        )

    except (
        jwt.PyJWTError,
        KeyError,
        ValueError
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
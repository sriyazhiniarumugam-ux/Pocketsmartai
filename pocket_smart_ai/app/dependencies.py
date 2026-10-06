from fastapi import Depends

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .security import get_user_id_from_token


security = HTTPBearer(
    auto_error=False
)


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db)
) -> User:

    user_id = get_user_id_from_token(
        credentials
    )

    user = db.get(
        User,
        user_id
    )

    if not user:

        from fastapi import HTTPException

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
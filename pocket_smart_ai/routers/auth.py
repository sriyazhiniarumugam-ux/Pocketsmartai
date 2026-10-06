from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import current_user
from app.models import User
from app.schemas import LoginRequest
from app.schemas import RegisterRequest
from app.security import create_access_token
from app.security import hash_password
from app.security import verify_password


router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    email = payload.email.lower()

    existing_user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(
            payload.password
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        user.id
    )

    return {
        "message": "Registration successful",
        "access_token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == payload.email.lower()
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        user.id
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.get("/session-info")
def session_info(
    user: User = Depends(current_user)
):

    return {
        "logged_in": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/logout")
def logout():

    return {
        "message": (
            "Logged out on client. "
            "Remove the saved token."
        )
    }
import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import current_user
from app.models import RecommendationHistory
from app.models import User
from app.schemas import HomeRequest
from app.schemas import PartyRequest
from services.ai_service import gemini_service


router = APIRouter(
    prefix="/api",
    tags=["Planners"]
)


def save_history(
    db: Session,
    user_id: int,
    planner: str,
    budget: float,
    request_data: dict,
    result: dict
):

    row = RecommendationHistory(
        user_id=user_id,
        planner=planner,
        budget=budget,
        request_json=json.dumps(
            request_data,
            ensure_ascii=False
        ),
        result_json=json.dumps(
            result,
            ensure_ascii=False
        )
    )

    db.add(row)
    db.commit()


@router.post("/generate-home")
def generate_home(
    payload: HomeRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    data = payload.model_dump()

    result = gemini_service.generate(
        "home",
        data
    )

    save_history(
        db=db,
        user_id=user.id,
        planner="home",
        budget=payload.budget,
        request_data=data,
        result=result
    )

    return result


@router.post("/generate-party")
def generate_party(
    payload: PartyRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    data = payload.model_dump()

    result = gemini_service.generate(
        "party",
        data
    )

    save_history(
        db=db,
        user_id=user.id,
        planner="party",
        budget=payload.budget,
        request_data=data,
        result=result
    )

    return result


@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(
        ...,
        gt=0,
        le=10_000_000
    ),

    occasion: str = Form(
        ...,
        min_length=2,
        max_length=100
    ),

    style: str = Form(
        "elegant",
        max_length=100
    ),

    outfit_color: str = Form(
        "",
        max_length=100
    ),

    notes: str = Form(
        "",
        max_length=1000
    ),

    outfit_image: UploadFile | None = File(
        None
    ),

    user: User = Depends(current_user),

    db: Session = Depends(get_db)
):

    image_bytes = None
    mime_type = None

    if outfit_image and outfit_image.filename:

        mime_type = (
            outfit_image.content_type
            or ""
        )

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if mime_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Upload JPG, PNG, "
                    "or WEBP image only"
                )
            )

        image_bytes = (
            await outfit_image.read()
        )

        max_size = (
            settings.max_upload_mb
            * 1024
            * 1024
        )

        if len(image_bytes) > max_size:

            raise HTTPException(
                status_code=413,
                detail=(
                    f"Image must be <= "
                    f"{settings.max_upload_mb} MB"
                )
            )

    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "outfit_color": outfit_color,
        "notes": notes
    }

    result = gemini_service.generate(
        "jewelry",
        data,
        image_bytes,
        mime_type
    )

    save_history(
        db=db,
        user_id=user.id,
        planner="jewelry",
        budget=budget,
        request_data=data,
        result=result
    )

    return result
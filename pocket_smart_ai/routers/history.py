import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import current_user
from app.models import RecommendationHistory
from app.models import User


router = APIRouter(
    prefix="/api",
    tags=["History"]
)


@router.get("/history")
def history(
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    rows = (
        db.query(
            RecommendationHistory
        )
        .filter(
            RecommendationHistory.user_id
            == user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .limit(50)
        .all()
    )

    return [
        {
            "id": row.id,
            "planner": row.planner,
            "budget": row.budget,
            "request": json.loads(
                row.request_json
            ),
            "result": json.loads(
                row.result_json
            ),
            "created_at": (
                row.created_at.isoformat()
            )
        }
        for row in rows
    ]


@router.get("/history/{history_id}")
def history_detail(
    history_id: int,
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    row = db.get(
        RecommendationHistory,
        history_id
    )

    if (
        not row
        or row.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="History item not found"
        )

    return {
        "id": row.id,
        "planner": row.planner,
        "budget": row.budget,
        "request": json.loads(
            row.request_json
        ),
        "result": json.loads(
            row.result_json
        ),
        "created_at": (
            row.created_at.isoformat()
        )
    }
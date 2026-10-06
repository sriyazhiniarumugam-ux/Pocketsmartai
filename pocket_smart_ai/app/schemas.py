from typing import Any
from typing import Literal

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    rooms: list[str] = Field(
        min_length=1
    )

    style: str = Field(
        default="modern",
        max_length=100
    )

    notes: str = Field(
        default="",
        max_length=1000
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=5000
    )

    event_type: str = Field(
        min_length=2,
        max_length=100
    )

    venue: str = Field(
        default="home",
        max_length=200
    )

    notes: str = Field(
        default="",
        max_length=1000
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = Field(
        min_length=2,
        max_length=100
    )

    style: str = Field(
        default="elegant",
        max_length=100
    )

    outfit_color: str = Field(
        default="",
        max_length=100
    )

    notes: str = Field(
        default="",
        max_length=1000
    )


class RecommendationItem(BaseModel):

    name: str

    category: str

    platform: str

    estimated_price: float = Field(
        ge=0
    )

    reason: str

    search_url: str

    priority: Literal[
        "high",
        "medium",
        "low"
    ] = "medium"


class RecommendationResponse(BaseModel):

    planner: Literal[
        "home",
        "party",
        "jewelry"
    ]

    budget: float

    budget_plan: list[
        dict[str, Any]
    ]

    summary: str

    recommendations: list[
        RecommendationItem
    ]

    tips: list[str]

    source: Literal[
        "gemini",
        "fallback"
    ]

    image_insight: str | None = None
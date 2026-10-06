from pathlib import Path

from fastapi import APIRouter
from fastapi import Request

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templates")
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@router.get(
    "/planner/{planner}",
    response_class=HTMLResponse
)
def planner_page(
    request: Request,
    planner: str
):

    if planner not in {
        "home",
        "party",
        "jewelry"
    }:

        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Planner not found"
        )

    return templates.TemplateResponse(
        request=request,
        name=f"{planner}_planner.html",
        context={"planner": planner}
    )


@router.get(
    "/history",
    response_class=HTMLResponse
)
def history_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={}
    )
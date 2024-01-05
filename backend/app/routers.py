import validators
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

from .config import get_settings
from .crud import (
    create_db_url,
    delete_db_url_by_secret_key,
    get_db_url_by_key,
    get_db_url_by_secret_key,
)
from .models import URL as model_url
from .schemas import URLBase, URLInfo
from .dependencies import DBSessionDep


router = APIRouter(
    prefix="/shorturl",
    responses={404: {"description": "Not found"}},
)


def get_admin_info(db_url: model_url) -> URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = router.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@router.post("/url", response_model=URLInfo)
async def create_url(
    url: URLBase, 
    db = DBSessionDep
):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=404, detail="Your provided URL is not valid")
    db_url = create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@router.get("/{url_key}")
async def forward_to_target_url(
    url_key: str, 
    request: Request, 
    db = DBSessionDep
):
    if db_url := await get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=404, detail=request)


@router.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=URLInfo,
)
async def get_url_info(
    secret_key: str, 
    request: Request, 
    db = DBSessionDep
):
    if db_url := await get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise HTTPException(status_code=404, detail=request)


@router.delete("/admin/{secret_key}")
async def delete_url(
    secret_key: str, 
    request: Request, 
    db = DBSessionDep
):
    if db_url := await delete_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise HTTPException(status_code=404, detail=request)

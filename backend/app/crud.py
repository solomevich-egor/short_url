from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import URL as model_url
from .schemas import URLBase

from . import keygen


def create_db_url(db: AsyncSession, url: URLBase) -> model_url:
    key = keygen.create_random_key()
    secret_key = keygen.create_random_key(length=8)
    db_url = model_url(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(instance=db_url)
    return db_url


async def get_db_url_by_key(db: AsyncSession, url_key: str) -> model_url:
    return (
        await db.scalars(
            select(model_url)
            .where(model_url.key == url_key)
        )
    ).first()


async def get_db_url_by_secret_key(db: AsyncSession, secret_key: str) -> model_url:
    return (
        await db.scalars(
            select(model_url)
            .where(model_url.secret_key == secret_key)
        )
    ).first()


async def delete_db_url_by_secret_key(db: AsyncSession, secret_key: str) -> model_url:

    db_url = await get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db.delete(db_url)
    return db_url

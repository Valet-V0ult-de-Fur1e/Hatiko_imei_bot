from typing import Optional, Union
from sqlalchemy import delete, insert, or_, select, update
from db.models.user.model import RoleEnum, User
from db.db import AsyncSessionLocal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session


async def user_exists(session: AsyncSession, tg_id: int) -> bool:
    return bool(await session.scalar(select(User.tg_id).where(User.tg_id == tg_id)))


async def atomic_create_user(session: AsyncSession, tg_id: int) -> dict:
    user = User(tg_id=tg_id)
    session.add(user)
    await session.flush()
    return {"id": tg_id, "whitelist": False}


async def turbo_update(session: AsyncSession, tg_id: int, status: bool) -> int:
    result = await session.execute(
        update(User)
        .where(User.tg_id == tg_id)
        .values(in_white_list=status)
        .execution_options(synchronize_session="fetch")
    )
    return result.rowcount

async def find_user_by_id_or_create_new(user_tg_id: int) -> dict:
    async with get_session() as session:
        if not await user_exists(session, user_tg_id):
            data = await atomic_create_user(session, user_tg_id)
            return {"message": "created", **data}
        
        result = await session.execute(
            select(User.tg_id, User.in_white_list)
            .where(User.tg_id == user_tg_id)
        )
        tg_id, whitelist = result.first()
        return {"message": "finded", "id": tg_id, "in_whitelist": whitelist}

async def update_user(user_tg_id: int, status: bool):
    async with get_session() as session:
        updated = await turbo_update(session, user_tg_id, status)
        if not updated:
            raise ValueError("User not exists")
        
        return {
            "message": "updated",
            "id": user_tg_id,
            "in_whitelist": status
        }

async def stealth_delete(identifier: Union[int, str]) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            delete(User).where(or_(
                User.tg_id == identifier,
                User.tg_name == identifier,
                User.email == identifier
            )).returning(User.id)
        )
        await session.commit()
        return bool(result.scalar())

async def get_users_by_roles(roles: list[RoleEnum]):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.role.in_(roles))
        )
        return [{
            "id": u.id,
            "tg_id": u.tg_id,
            "role": u.role.value
        } for u in result.scalars()]
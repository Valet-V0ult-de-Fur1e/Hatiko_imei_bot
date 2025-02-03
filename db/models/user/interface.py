from sqlalchemy import select
from db.models.user.model import User
from db.db import AsyncSessionLocal

async def find_user_by_id_or_create_new(user_tg_id: int) -> dict:
    async with AsyncSessionLocal() as session:
        check_user = True
        result = await session.execute(select(User).where(User.tg_id == user_tg_id))
        user:User = result.scalars().first()
        if user is None:
            check_user = False
            new_user = User(tg_id=user_tg_id)
            session.add(new_user)
        await session.commit()
        return { 
                "message": "finded" if check_user else "created",
                "id": (user if check_user else new_user).tg_id,
                "in_whitelist": (user if check_user else new_user).in_white_list
                }

async def update_user(user_tg_id: int, user_in_white_list_status: bool):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.tg_id == user_tg_id))
        user:User = result.scalars().first()
        user.in_white_list = user_in_white_list_status
        print(user)
        session.add(user)
        await session.commit()
        return { 
                "message": "updated",
                "id": user.tg_id,
                "in_whitelist": user.in_white_list
                }
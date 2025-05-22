import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .users_table import UsersTable
from .models import AddUserModel, UserModel


class UsersTableInterface:
    parent_table = UsersTable

    @staticmethod
    async def add_user(add_user_model: AddUserModel, session: AsyncSession = None) -> None:
        session.add(
            UsersTable(
                email=add_user_model.email,
                phone_number=add_user_model.phone_number,
                password=add_user_model.password,
                secure_code="".join([random.choice(string.ascii_letters) for _ in range(64)]),
                secret=add_user_model.secret
            )
        )
        await session.commit()

    @staticmethod
    async def get_user(uuid: str, secure_code: str, session: AsyncSession = None) -> UserModel:
        user = (await session.execute(
            select(UsersTable).where(UsersTable.id == uuid and UsersTable.secure_code == secure_code)
        )).scalars().first()
        return UserModel(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            secret=user.secret,
            secure_code=user.secure_code,
            password=user.password
        )

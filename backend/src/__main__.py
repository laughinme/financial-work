import asyncio

from utils.auth_2fa import QRCodeGenerator2FA, OTPGenerator

from database.relational_db import RelationalDatabase
from database.relational_db.tables.users_table import UsersTableInterface, AddUserModel


async def main():
    database = RelationalDatabase(UsersTableInterface)
    await database.create_tables()

    db: UsersTableInterface = database

    # user = await db.get_user(*args)
    # await QRCodeGenerator2FA.create_qr(user.secret, user.email)

if __name__ == "__main__":
    asyncio.run(main())

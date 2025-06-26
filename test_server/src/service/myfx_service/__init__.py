from .service import MyFXService

async def get_myfxservice() -> MyFXService:
    return MyFXService()

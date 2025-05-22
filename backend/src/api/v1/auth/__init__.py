from fastapi import APIRouter

from .authentication import router as register_router


router = APIRouter(prefix='/auth')

router.include_router(register_router)

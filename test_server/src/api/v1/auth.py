from fastapi import APIRouter, Query

router = APIRouter()

@router.get('/login.json')
async def login(
    email: str = Query(...), 
    password: str = Query(...)
):
    return {"error": False, "message": "", "session": "session_123"}

@router.get('/logout.json')
async def logout(
    session: str = Query(...)
):
    return {"error": False, "message": "ok"}

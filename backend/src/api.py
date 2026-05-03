from fastapi import FastAPI, APIRouter, Depends
from typing import Dict

from .database.db import get_db
from .entities.user_entity import UserEntity
from .auth.auth_controller import router as auth_router
from .users.users_controller import router as users_router

api = FastAPI()

router = APIRouter(
)

@router.get("/")
async def RootEntry() -> Dict[str, str]:
    return {
        "message": "Hello World!"
    }

api.include_router(router=router)
api.include_router(router=auth_router)
api.include_router(router=users_router)
import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from fastapi.staticfiles import StaticFiles

from .auth.auth_controller import router as auth_router
from .users.users_controller import router as users_router
from .products.products_controller import router as products_router
from .carts.carts_controller import router as carts_router
from .orders.orders_controller import router as orders_router
from .recommendations.recommendations_controller import router as recommendations_router

api = FastAPI()

os.makedirs("static/uploads", exist_ok=True)
api.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:5173"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
api.include_router(router=products_router)
api.include_router(router=carts_router)
api.include_router(router=orders_router)
api.include_router(router=recommendations_router)
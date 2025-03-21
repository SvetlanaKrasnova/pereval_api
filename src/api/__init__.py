from fastapi import APIRouter

from src.api.v1.pereval import pereval_router

api_router = APIRouter()
api_router.include_router(pereval_router)

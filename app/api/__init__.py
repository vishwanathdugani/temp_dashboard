from fastapi import APIRouter

from .endpoints import temperature

router = APIRouter()

router.include_router(temperature.router, prefix="/temperatures", tags=["temperatures"])

import pymongo.errors
from fastapi import APIRouter, HTTPException, status

from services.movement_services import MovementServices

movements_router = APIRouter()


@movements_router.get("/", summary="List all movements", tags=["Movements"])
async def get_movements():
    try:
        result = await MovementServices.get_movements()
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can't get movements."
        )

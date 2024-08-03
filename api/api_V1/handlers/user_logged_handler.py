from fastapi import HTTPException
import pymongo.errors

from api.deps.user_deps import get_current_user
from models.user_model import User
from fastapi import APIRouter, Depends, status

from services.user_loged_services import UserLoggedServices

user_logged_router = APIRouter()


@user_logged_router.get("/receipts", summary="Get all receipts", tags=["User Logged"])
async def get_receipts_from_user_logged(owner: User = Depends(get_current_user)):
    try:
        result = await UserLoggedServices.get_receipt_by_user_uuid(owner.user_id)
        return result
    except pymongo.errors.OperationFailure as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@user_logged_router.get("/athletes", summary="Get all athletes", tags=["User Logged"])
async def get_athletes_from_user_logged(owner: User = Depends(get_current_user)):
    try:
        result = await UserLoggedServices.get_athletes_by_user_uuid(owner.user_id)
        return result
    except pymongo.errors.OperationFailure as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

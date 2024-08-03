from uuid import UUID
import pymongo.errors
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from api.deps.user_deps import get_current_user
from models.role_model import Role
from models.user_model import User
from schemas.user_schema import UserAuth, UserUpdate
from services.change_user_avatar_service import ChangeUserAvatarService
from services.user_services import UserService

user_router = APIRouter()


@user_router.post('/create', summary="Create new user.", tags=["User"])
async def create_user(data: UserAuth):
    try:
        result = await UserService.create_user(data)
        return result

    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with that username or email already exists."
        )


@user_router.put('/avatar/{user_id}', summary="Update user avatar.", tags=["User"])
async def update_user_avatar(user_id: UUID, file: UploadFile = File(...)):
    try:
        result = await ChangeUserAvatarService.change_avatar_for_user(user_id, file)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user you want to update not exists."
        )


@user_router.put('/update', summary="Update user", tags=["User"])
async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
    try:
        return await UserService.update_user(user.user_id, data, None)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user you want to update not exists."
        )


@user_router.get('/me', summary="Get the user logged in.", tags=["User"])
async def get_me(user: User = Depends(get_current_user)):
    try:
        if user:
            role = await Role.find_one(Role.id == user.role)
            if role:
                user.role = role.name
        return user
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user is not logged in."
        )


@user_router.get('/by_object_id/{user_id}', summary="Get user by ObjectId.", tags=["User"])
async def get_user_by_object_id(user_id: PydanticObjectId):
    try:
        result = await UserService.get_user_by_object_id(user_id)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is not user whith that ID."
        )


@user_router.get('/list', summary='Get all users without authentication.', tags=["User"])
async def list_users():
    try:
        result = UserService.get_all_users()
        return await result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There are not user entries."
        )


@user_router.get('/list_as_admin', summary='Get all users without authentication as admin.', tags=["User"])
async def list_users_as_admin():
    try:
        result = UserService.get_all_users_as_admin()
        return await result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There are not user entries."
        )


@user_router.put('/update/admin/{user_id}', summary='Update user by ID.', tags=["User"])
async def update_user_as_admin(user_id: UUID, data: UserUpdate, owner: User = Depends(get_current_user)):
    try:
        result = UserService.update_user(user_id, data, owner)
        return await result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't edit the user."
        )


@user_router.delete('/delete/{user_id}', summary='Delete user by id.', tags=["User"])
async def delete_user(user_id: UUID, owner: User = Depends(get_current_user)):
    try:
        result = UserService.delete_user(user_id, owner)
        return await result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't delete the user."
        )

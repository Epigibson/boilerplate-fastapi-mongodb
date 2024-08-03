from uuid import UUID

import pymongo.errors
from fastapi import HTTPException, status, APIRouter
from schemas.role_schema import RoleCreate, RoleUpdate, RolOut
from services.role_services import RoleService

role_router = APIRouter()


@role_router.post("/create", summary="Create a new role", tags=["Role"])
async def create(data: RoleCreate):
    try:
        result = await RoleService.create(data)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't create a new role"
        )


@role_router.get("/", summary="List all roles", tags=["Role"], response_model=list[RolOut])
async def get_list():
    try:
        result = await RoleService.list()
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't list all roles"
        )


@role_router.get("/{role_id}", summary="Get a role by id", tags=["Role"])
async def retrieve(role_id: UUID):
    try:
        result = await RoleService.retrieve(role_id)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't get a role by id"
        )


@role_router.get("/by_name/{role_name}", summary="Get a role by name", tags=["Role"])
async def retrieve_name(role_name: str):
    try:
        result = await RoleService.retrieve_name(role_name)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can't get a role or not exist with the name {role_name}"
        )


@role_router.get("/user_register/{role_name}", summary="Get a role by name to register user", tags=["Role"])
async def retrieve_name(role_name: str):
    try:
        result = await RoleService.retrieve_name_for_user_create(role_name)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can't get a role or not exist with the name {role_name}"
        )


@role_router.put("/{role_id}", summary="Update a role by id", tags=["Role"])
async def update(role_id: UUID, data: RoleUpdate):
    try:
        result = await RoleService.update(role_id, data)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't update a role by id"
        )


@role_router.delete("/{role_id}", summary="Delete a role by id", tags=["Role"])
async def delete(role_id: UUID):
    try:
        result = await RoleService.delete(role_id)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't delete a role by id"
        )

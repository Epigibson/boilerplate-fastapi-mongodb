from datetime import datetime
import pymongo.errors
from fastapi import APIRouter, HTTPException, status
from pytz import timezone

from schemas.configurations_schema import ConfigurationsCreate, ConfigurationsUpdate
from services.configuration_services import ConfigurationServices

configuration_router = APIRouter()


@configuration_router.post("/create", summary="Create a new configuration", tags=["Configuration"])
async def create(data: ConfigurationsCreate):
    try:
        result = await ConfigurationServices.create_configuration(data)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't create the configuration"
        )


@configuration_router.get("/", summary="List of configurations", tags=["Configuration"])
async def get_list():
    try:
        result = await ConfigurationServices.get_configuration()
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't get the configuration"
        )


@configuration_router.put("/", summary="Update configuration", tags=["Configuration"])
async def update(data: ConfigurationsUpdate):
    try:
        result = await ConfigurationServices.update_configuration(data)
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't update the configuration"
        )


@configuration_router.delete("/", summary="Delete configuration",
                             tags=["Configuration"])
async def delete():
    try:
        result = await ConfigurationServices.delete_configuration()
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't delete the configuration"
        )


@configuration_router.get("/horario/", summary="Horario",
                          tags=["Configuration"])
async def horario():
    try:
        horario_uno = datetime.now()
        horario_dos = datetime.utcnow()
        return {
            "Horario uno": horario_uno,
            "Horario dos": horario_dos,
            "Horario correcto": datetime.now(timezone('America/Mexico_City')),
        }
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't delete the configuration"
        )

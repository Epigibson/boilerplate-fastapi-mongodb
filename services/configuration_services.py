from uuid import UUID
from fastapi import HTTPException, status
from models.configurations_model import Configurations
from schemas.configurations_schema import ConfigurationsCreate, ConfigurationsUpdate


class ConfigurationServices:

    @staticmethod
    async def create_configuration(data: ConfigurationsCreate):
        check_configuration = await ConfigurationServices.get_configuration()
        if check_configuration:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe una configuracion")
        result = Configurations(**data.dict())
        return await result.insert()

    @staticmethod
    async def get_configuration():
        configuration = await Configurations.find_all().to_list()
        result = None
        if configuration:
            result = configuration[0]
        return result

    @staticmethod
    async def get_configuration_receipts():
        configuration = await Configurations.find_all().to_list()
        if not configuration:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe configuracion")
        result = configuration[0].generation_receipts
        return result

    @staticmethod
    async def get_configuration_by_id() -> Configurations:
        result = await ConfigurationServices.get_configuration()
        return result

    @staticmethod
    async def update_configuration(data: ConfigurationsUpdate) -> Configurations:
        result = await ConfigurationServices.get_configuration()
        await result.update({"$set": data.dict(exclude_unset=True)})
        result.commit()
        return result

    @staticmethod
    async def delete_configuration() -> Configurations:
        result = await ConfigurationServices.get_configuration()
        await result.delete()
        return result

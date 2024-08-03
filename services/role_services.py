from uuid import UUID

from models.permission_model import Permission
from models.role_model import Role
from schemas.role_schema import RoleCreate, RoleUpdate


class RoleService:

    @staticmethod
    async def create(data: RoleCreate):
        result = Role(**data.dict())
        await result.insert()
        return result

    @staticmethod
    async def retrieve(role_id: UUID):
        result = await Role.find_one(Role.role_id == role_id)
        return result

    @staticmethod
    async def retrieve_name(role_name: str):
        result = await Role.find_one(Role.name == role_name)
        return result

    @staticmethod
    async def retrieve_name_for_user_create(role_name: str):
        result = await Role.find_one(Role.name == role_name)
        return result.id

    @staticmethod
    async def list():
        roles = await Role.find_all().to_list()
        return roles

    @staticmethod
    async def update(role_id: UUID, data: RoleUpdate):
        result = await RoleService.retrieve(role_id)
        await result.update({"$set": data.dict(exclude_unset=True)})
        result.commit()
        return result

    @staticmethod
    async def delete(role_id: UUID):
        result = await RoleService.retrieve(role_id)
        await result.delete()
        message = f"Role {role_id} deleted successfully"
        return message

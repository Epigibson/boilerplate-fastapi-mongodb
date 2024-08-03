from typing import Optional, List
from uuid import UUID
import pymongo.errors
from beanie import PydanticObjectId
from fastapi import UploadFile, File

from cloudinary.uploader import upload

from core.security import get_password, verify_password
from models.choices.action_types import ActionTypes
from models.choices.modeules_choices import ModuleTypes
from models.choices.movemen_type import MovementType
from models.choices.user_types import Usertype
from models.role_model import Role
from models.user_counter import UserCounter
from models.user_model import User
from schemas.user_schema import UserAuth, UserUpdate
from services.movement_services import MovementServices
from services.role_services import RoleService


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        normal_role = await RoleService.retrieve_name_for_user_create("Normal")
        user_count = await UserCounter.find_one()
        email_verification_user = await UserService.get_user_by_email(user.email)
        generate_username = await UserService.generate_username(user.email)
        user_in = User(
            email=user.email,
            username=generate_username,
            hashed_password=get_password(user.password) if user.password else None,
            role=user.role if user.role else normal_role,
            mobile=user.mobile,
            phone=user.phone,
        ) if not email_verification_user else email_verification_user

        if not email_verification_user:
            try:
                await user_in.insert()
            except Exception as e:
                print(f"Error al insertar el usuario: {e}")

        user_count.counter += 1
        await user_in.save()
        await user_count.save()
        return user_in

    @staticmethod
    async def create_image_profile(file: UploadFile = File(...)):
        result = upload(file.file.read(), folder="be_plus/")
        image = result['url']
        return image

    @staticmethod
    async def generate_username(user_email: str):
        username = user_email.split("@")[0]
        return username

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        await MovementServices.create_movement(
            MovementType.login,
            ActionTypes.login,
            ModuleTypes.auth,
            user.id,
            "authentication",
            user.id,
            user.tutors_name_one or user.username or user.name)
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        if user:
            role = await Role.find_one(Role.id == user.role)
            if role:
                user.role = role.name
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        user = await User.find_one(User.username == username)
        if user:
            role = await Role.find_one(Role.id == user.role)
            if role:
                user.role = role.name
        return user

    @staticmethod
    async def get_all_users() -> List[User]:
        users = await User.find(User.user_type == Usertype.user).to_list()
        if users:
            for user in users:
                role = await Role.find_one(Role.id == user.role)
                if role:
                    user.role = role.name
        return users

    @staticmethod
    async def get_all_users_as_admin() -> List[User]:
        users = await User.find().to_list()
        return users

    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == user_id)
        if user:
            role = await Role.find_one(Role.id == user.role)
            if role:
                user.role = role.name
        return user

    @staticmethod
    async def get_user_by_object_id(user_id: PydanticObjectId):
        user = await User.find_one(User.id == user_id)
        if user:
            role = await Role.find_one(Role.id == user.role)
            if role:
                user.role = role.name
        return user

    @staticmethod
    async def update_user(user_id: UUID, data: UserUpdate, owner: Optional[User]):
        user = await User.find_one(User.user_id == user_id)
        if not user:
            raise pymongo.errors.OperationFailure("User not found.")
        await user.update({"$set": data.dict(exclude_unset=True)})
        await MovementServices.create_movement(
            MovementType.coach_info_edit,
            ActionTypes.update,
            ModuleTypes.coaches,
            owner.id,
            "coaches",
            user.id,
            user.tutors_name_one or user.name)
        return user

    @staticmethod
    async def delete_user(user_id: UUID, owner: User) -> None:
        user = await User.find_one(User.user_id == user_id)
        if not user:
            raise pymongo.errors.OperationFailure("User not found.")
        await user.delete()
        await MovementServices.create_movement(
            MovementType.coach_delete,
            ActionTypes.delete,
            ModuleTypes.coaches,
            owner.id,
            "coaches",
            user.id,
            user.tutors_name_one or user.name)
        return

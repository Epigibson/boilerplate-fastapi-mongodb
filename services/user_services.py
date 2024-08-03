from datetime import datetime
from typing import Optional, List
from uuid import UUID
import pymongo.errors
from beanie import PydanticObjectId
from fastapi import UploadFile, File, Query, HTTPException, status

from cloudinary.uploader import upload
from pymongo import DESCENDING

from core.filter_helper import FilterHelperService
from core.security import get_password, verify_password
from core.validate_dates_filter import ValidateDatesFilter
from models.athlete_model import Athlete
from models.choices.action_types import ActionTypes
from models.choices.modeules_choices import ModuleTypes
from models.choices.movemen_type import MovementType
from models.choices.user_types import Usertype
from models.role_model import Role
from models.user_counter import UserCounter
from models.user_model import User
from schemas.filters_schema import FilterDates
from schemas.system_user_schema import SystemUserCreate
from schemas.user_schema import UserAuth, UserUpdate
from services.movement_services import MovementServices
from services.role_services import RoleService


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        normal_role = await RoleService.retrieve_name_for_user_create("Normal")
        user_count = await UserCounter.find_one()
        email_verification_user = await UserService.get_user_by_email(user.email)
        generate_username = await UserService.generate_username(
            user.email)
        user_in = User(
            email=user.email,
            username=generate_username,
            hashed_password=get_password(user.password) if user.password else None,
            role=user.role if user.role else normal_role,
            mobile=user.mobile,
            phone=user.phone,
            tutors_name_one=user.tutors_name_one if user.tutors_name_one else "",
            tutors_name_two=user.tutors_name_two if user.tutors_name_two else "",
        ) if not email_verification_user else email_verification_user

        if not email_verification_user:
            try:
                await user_in.insert()
            except Exception as e:
                print(f"Error al insertar el usuario: {e}")
        athlete_in = Athlete(
            name=user.name,
            gender=user.gender,
            age=user.age,
            sport_preference=user.sport_preference,
            hobbies=user.hobbies,
            user_type=Usertype.user,
            user_count=user_count.counter,
        )
        await athlete_in.insert()
        helper_tuition = int(athlete_in.user_count)
        athlete_in.tuition = await UserService.generate_tuition(helper_tuition)
        user_in.athletes.append(athlete_in.id)
        user_count.counter += 1
        await athlete_in.save()
        await user_in.save()
        await user_count.save()
        return {'user': user_in, 'athlete': athlete_in}

    @staticmethod
    async def create_user_system(user: SystemUserCreate, user_type: str, owner: User):
        generate_username = await UserService.generate_username(
            user.email)
        role = await RoleService.retrieve_name("Manager" if user_type == "Manager" else "Admin")
        user_in = User(
            email=user.email,
            username=generate_username,
            hashed_password=get_password(user.password),
            role=role.id,
            user_type=user_type,
            tutors_name_one=user.name if user.name else "",
            tutors_name_two=user.name if user.name else "",
        )
        await user_in.insert()
        await MovementServices.create_movement(MovementType.system_user_created,
                                               ActionTypes.create,
                                               ModuleTypes.users,
                                               owner.id,
                                               "Users",
                                               user_in.id,
                                               f"Se crea el nuevo usuario {user_in.name} para el sistema,"
                                               f"con el rol de {role.name}, "
                                               f"por {owner.tutors_name_one or owner.tutors_name_two or owner.username}")
        return user_in

    @staticmethod
    async def create_couch(couch: UserAuth, owner: User):
        role = await Role.find_one(Role.name == "Couch")
        couch = User(
            email=couch.email,
            hashed_password=get_password("123456"),
            role=role.id,
            name=couch.name,
            user_type=Usertype.couch,
            gender=couch.gender,
            age=couch.age,
            groups=couch.groups,
            tutors_name_one=couch.name,
            tutors_name_two=couch.name,
        )
        await couch.insert()
        couch.username = await UserService.generate_username(couch.email)
        await couch.save()
        await MovementServices.create_movement(MovementType.coach_created,
                                               ActionTypes.create,
                                               ModuleTypes.coaches,
                                               owner.id,
                                               "coaches",
                                               couch.id,
                                               couch.tutors_name_one or couch.name)
        return couch

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
    async def generate_tuition(user_count: int):
        user_count_int = int(user_count)
        date = datetime.now()
        # Asegúrate de que name, username, y birthday están disponibles
        if date:
            raw_tuition = f"{date.year}{date.month:02d}{user_count_int:03d}"
            # Por ejemplo, usando los primeros 10 caracteres de un hash como matrícula
            tuition = raw_tuition
        else:
            raise ValueError("Name and username must be set to generate tuition")

        return tuition

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        await MovementServices.create_movement(MovementType.login,
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
    async def get_all_users_with_range_dates(data: Optional[FilterDates]) -> List[User]:
        documents = await ValidateDatesFilter.validate_dates(data.init_date, data.end_date, User, 'desc', 'created_at')
        users = [User(**doc.dict()) for doc in documents]
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
    async def get_users_inscribed_and_active():
        helper: bool = True
        result = await User.find(User.user_type == Usertype.user, User.is_inscribed == helper,
                                 User.status == helper).to_list()
        if result:
            for user in result:
                role = await Role.find_one(Role.id == user.role)
                if role:
                    user.role = role.name
        return result

    @staticmethod
    async def get_couches(data: Optional[FilterDates] = None) -> Optional[list[User]]:
        if not data:
            couches = await User.find(User.user_type == Usertype.couch).to_list()
            return couches
        documents = await ValidateDatesFilter.validate_dates(data.init_date, data.end_date, User, 'desc', 'created_at')
        users = [User(**doc.dict()) for doc in documents]
        couches = [user for user in users if user.user_type == Usertype.couch]
        return couches

    @staticmethod
    async def get_inscriptions():
        inscriptions = await User.find(User.is_inscribed == True).to_list()
        return inscriptions

    @staticmethod
    async def add_balance_amount_to_user(user_id: UUID, balance_amount: float, payment_method: str, owner: User):
        user = await UserService.get_user_by_id(user_id)
        user.positive_balance += balance_amount
        await user.save()
        await MovementServices.create_movement(MovementType.add_balance_to_user,
                                               ActionTypes.update,
                                               ModuleTypes.users,
                                               owner.id,
                                               "users",
                                               user.id,
                                               f"Responsable de operacion: "
                                               f"{owner.tutors_name_one or owner.name or owner.username}. "
                                               f"Se adiciona la cantidad de: ${balance_amount} "
                                               f"MXN de saldo al usuario en {payment_method} "
                                               f"{user.tutors_name_one or user.name or user.username}")
        return user

    @staticmethod
    async def update_balance_amount_to_user(user_id: UUID, balance_amount: float, payment_method: str, owner: User):
        user = await UserService.get_user_by_id(user_id)
        user.positive_balance = balance_amount
        await user.save()
        await MovementServices.create_movement(MovementType.add_balance_to_user,
                                               ActionTypes.update,
                                               ModuleTypes.users,
                                               owner.id,
                                               "users",
                                               user.id,
                                               f"Responsable de operacion: "
                                               f"{owner.tutors_name_one or owner.name or owner.username}. "
                                               f"Se adiciona la cantidad de: ${balance_amount} "
                                               f"MXN de saldo al usuario en {payment_method} "
                                               f"{user.tutors_name_one or user.name or user.username}")
        return user

    @staticmethod
    async def subtract_balance_amount_to_user(user_id: UUID, balance_amount: float):
        user = await UserService.get_user_by_id(user_id)
        user.positive_balance -= balance_amount
        await user.save()
        return user

    @staticmethod
    async def edit_balance_amount_to_user(user_id: UUID, balance_amount: float):
        user = await UserService.get_user_by_id(user_id)
        user.positive_balance = balance_amount
        await user.save()
        return user

    @staticmethod
    async def update_user(user_id: UUID, data: UserUpdate, owner: Optional[User]):
        user = await User.find_one(User.user_id == user_id)
        if not user:
            raise pymongo.errors.OperationFailure("User not found.")
        await user.update({"$set": data.dict(exclude_unset=True)})
        await MovementServices.create_movement(MovementType.coach_info_edit,
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
        await MovementServices.create_movement(MovementType.coach_delete,
                                               ActionTypes.delete,
                                               ModuleTypes.coaches,
                                               owner.id,
                                               "coaches",
                                               user.id,
                                               user.tutors_name_one or user.name)
        return

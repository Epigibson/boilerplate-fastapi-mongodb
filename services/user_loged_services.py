from uuid import UUID
from models.receipts_model import Receipts
from services.athlete_service import AthleteServices
from services.user_services import UserService


class UserLoggedServices:

    @staticmethod
    async def get_receipt_by_user_uuid(owner: UUID):
        user = await UserService.get_user_by_id(owner)
        receipts = await Receipts.find(Receipts.user_id == user.id).to_list()
        return receipts

    @staticmethod
    async def get_athletes_by_user_uuid(owner: UUID):
        user = await UserService.get_user_by_id(owner)
        athletes = await AthleteServices.get_athletes_by_user_id(user.id)
        return athletes

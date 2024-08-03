from beanie import PydanticObjectId
from models.choices.action_types import ActionTypes
from models.choices.modeules_choices import ModuleTypes
from models.choices.movemen_type import MovementType
from models.movement_model import Movement
from models.user_model import User


class MovementServices:

    @staticmethod
    async def create_movement(movement_type: MovementType,
                              action_type: ActionTypes,
                              module: ModuleTypes,
                              responsible_id: PydanticObjectId,
                              model_affected: str,
                              model_field_id: PydanticObjectId,
                              model_field_helper: str):
        responsible = await User.find_one(User.id == responsible_id)

        movement_in = Movement(
            type=movement_type,
            action=action_type,
            module=module,
            responsible_id=responsible_id,
            responsible_name=responsible.tutors_name_one or responsible.tutors_name_two or responsible.name,
            model_affected=model_affected,
            model_field_id=model_field_id,
            model_field_helper=model_field_helper,
        )
        await movement_in.insert()
        return movement_in

    @staticmethod
    async def get_movements():
        result = await Movement.find_all().to_list()
        return result

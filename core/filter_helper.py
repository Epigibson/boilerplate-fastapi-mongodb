import re
from typing import Union

from beanie import PydanticObjectId


class FilterHelperService:

    @staticmethod
    def build_filter_conditions(**filter_args: Union[str, int, float, bool, PydanticObjectId]) \
            -> list[dict]:
        filter_conditions = []
        init_date = filter_args.pop("init_date", None)
        end_date = filter_args.pop("end_date", None)

        if init_date and end_date:
            filter_conditions.append({
                "created_at": {"$gte": init_date, "$lte": end_date}
            })
        for key, value in filter_args.items():
            if value is not None:
                if isinstance(value, str):
                    # Convert the value to a regex pattern
                    regex_pattern = f".*{re.escape(value)}.*"
                    filter_conditions.append({key: {"$regex": regex_pattern, "$options": "i"}})
                elif isinstance(value, PydanticObjectId):
                    """
                        Si el valor es de tipo PydanticObjectId, 
                        simplemente agregarlo a las condiciones sin modificarlo.
                    """
                    filter_conditions.append({key: value})
                else:
                    # For other types, just add the key and value to the filter_conditions list
                    filter_conditions.append({key: value})
        return filter_conditions

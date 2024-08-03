from datetime import datetime
from typing import Type, Optional
from beanie import Document
from fastapi import HTTPException, status
from pymongo import DESCENDING, ASCENDING
from core.filter_helper import FilterHelperService


class ValidateDatesFilter:

    @staticmethod
    async def validate_dates(
            init_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            model: Type[Document] = None,
            order: str = 'asc',
            base_field: str = 'created_at'
    ) -> list[Document]:

        """
                Valida las fechas y construye una consulta a la base de datos con filtros y
                ordenación.

                :param init_date: Fecha inicial para el filtro.
                :param end_date: Fecha final para el filtro.
                :param model: Modelo de base de datos a consultar.
                :param order: Orden de los resultados ('asc' o 'desc').
                :param base_field: Campo base para la ordenación.
                :return: Lista de documentos que cumplen con los criterios de filtro y ordenación.
                :raises HTTPException: Sí ocurre un error durante la consulta.
        """

        if init_date and end_date and init_date > end_date:
            raise ValueError("init_date must be less than or equal to end_date")

        if not model:
            raise ValueError("model is required")

        referred_field = base_field

        data_filter = {}
        if init_date and end_date:
            data_filter[referred_field] = {"$gte": init_date, "$lte": end_date}

        filter_conditions = FilterHelperService.build_filter_conditions(**data_filter)
        query = {"$and": filter_conditions} if filter_conditions else {}

        order_data = DESCENDING if order == 'desc' else ASCENDING

        try:
            result = await model.find(query).sort([(referred_field, order_data)]).to_list()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        return result

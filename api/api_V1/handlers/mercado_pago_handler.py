from uuid import UUID

from fastapi import APIRouter, Depends

from api.deps.user_deps import get_current_user
from models.user_model import User
from services.mercado_pago_checkout_service import MercadoPagoService

mercado_pago_router = APIRouter()


@mercado_pago_router.post("/mercado_pago/webhook", tags=["mercado pago"])
async def mercado_pago_webhook(product_id: UUID, user: UUID):
    try:
        result = await MercadoPagoService.create_preference(product_id, user)
        return result
    except Exception as e:
        print(e)
        return {"message": "Error"}

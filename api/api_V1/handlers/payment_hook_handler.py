import mercadopago
import pymongo.errors
from fastapi import APIRouter, HTTPException, status
from core.config import settings
from schemas.payment_data_schema import PaymentData

payment_hook_router = APIRouter()


@payment_hook_router.post("/", summary="Payment hook", tags=["Payment hook"])
async def payment_hook(payment_data: PaymentData):
    try:
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        payment_payload = {
            "action": payment_data.action,
            "api_version": payment_data.api_version,
            "data": payment_data.data,
            "date_created": payment_data.date_created,
            "id": payment_data.id,
            "live_mode": payment_data.live_mode,
            "type": payment_data.type,
            "user_id": payment_data.user_id
        }

        payment_response = sdk.payment().create(payment_payload)
        payment = payment_response["response"]

        if payment_response["status"] != "approved":
            return {"status": "failure", "detail": "Payment was not approved"}

        return {"status": "success" + payment}

    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Operation failed with the database"
        )

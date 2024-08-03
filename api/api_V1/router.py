from fastapi import APIRouter
from api.api_V1.handlers import user_handler
from api.api_V1.handlers import configurations_handler
from api.api_V1.handlers import notifications_handler
from api.api_V1.handlers import role_handler
from api.api_V1.handlers import permission_handler
from api.api_V1.handlers import mercado_pago_handler
from api.api_V1.handlers import payment_hook_handler
from api.api_V1.handlers import movements_handler
from api.api_V1.handlers import user_logged_handler
from api.auth.jwt import auth_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth', tags=["Auth"])
router.include_router(user_handler.user_router, prefix='/user')
router.include_router(role_handler.role_router, prefix='/role')
router.include_router(permission_handler.permission_router, prefix='/permission')
router.include_router(configurations_handler.configuration_router, prefix='/configuration')
router.include_router(notifications_handler.notification_router, prefix='/notification')
router.include_router(mercado_pago_handler.mercado_pago_router, prefix='/mercado_pago')
router.include_router(payment_hook_handler.payment_hook_router, prefix='/payment_hooks')
router.include_router(movements_handler.movements_router, prefix='/movements')
router.include_router(user_logged_handler.user_logged_router, prefix='/user_logged')

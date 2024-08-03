import asyncio
from datetime import datetime
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pytz import timezone
from starlette.middleware.cors import CORSMiddleware
from api.api_V1.router import router
from core.config import settings
from core.description import DESCRIPTION
from core.periodic_task_runner import periodic_task_runner
from core.update_fields import update_fields, verify_dates
from docs import tags_metadata
from models.notifications_model import Notifications
from models.configurations_model import Configurations
from models.receipts_model import Receipts
from models.user_model import User
from models.role_model import Role
from models.permission_model import Permission
from models.category_model import Category
from models.product_model import Product, Discounts
from models.user_counter import UserCounter
from models.movement_model import Movement
from models.sales_history_model import SalesHistory
from models.balance_history_model import BalanceHistory
from prometheus_client import Counter, Gauge, Histogram, Summary, make_asgi_app

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=DESCRIPTION,
    version="1.0.0(Alpha)",
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=False
)

# Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNTER = Counter('request_count', 'Total request count')
REQUEST_IN_PROGRESS = Gauge('request_in_progress', 'Number of requests in progress')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')


@app.get("/", summary="Welcome!", tags=["Home"])
async def read_root():
    local_tz = timezone(settings.TIMEZONE)
    now = datetime.now(local_tz)
    return {
        # "current_time": now.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
        # "message": "¡Hello, welcome to SportManager From AIS!"
        "QUE ONDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    }


@app.on_event("startup")
async def app_init():
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).SportManager

    await init_beanie(
        database=db_client,
        document_models=[
            User,
            Role,
            Permission,
            Notifications,
            Configurations,
            Product,
            Discounts,
            Receipts,
            Category,
            UserCounter,
            Movement,
            SalesHistory,
            BalanceHistory,
        ]
    )

    # Call function to update new fields.
    await update_fields()
    await verify_dates()
    asyncio.create_task(periodic_task_runner())


# Mount the Prometheus metrics endpoint
prometheus_app = make_asgi_app()
app.mount("/metrics", prometheus_app)

app.include_router(router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

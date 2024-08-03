import asyncio
from typing import Optional

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
from api.api_V1.router import router
from core.config import settings
from core.description import DESCRIPTION
from core.periodic_task_runner import periodic_task_runner
from core.update_fields import update_fields
from docs import tags_metadata
from models.notifications_model import Notifications
from models.configurations_model import Configurations
from models.user_model import User
from models.role_model import Role
from models.permission_model import Permission
from models.user_counter import UserCounter
from models.movement_model import Movement
from prometheus_client import Counter, Gauge, Histogram, Summary, make_asgi_app


class CustomFastAPI(FastAPI):
    mongodb_client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorClient] = None
    periodic_task: Optional[asyncio.Task] = None


app = CustomFastAPI(
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
@REQUEST_TIME.time()
@REQUEST_IN_PROGRESS.track_inprogress()
async def read_root():
    REQUEST_COUNTER.inc()
    return {"QUE ONDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"}


@app.on_event("startup")
async def app_init():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    app.db = app.mongodb_client.EcommerceTangram

    await init_beanie(
        database=app.db,
        document_models=[
            User,
            Role,
            Permission,
            Notifications,
            Configurations,
            UserCounter,
            Movement,
        ]
    )

    # Call function to update new fields.
    await update_fields()

    # Iniciar la tarea periódica
    app.periodic_task = asyncio.create_task(periodic_task_runner())


@app.on_event("shutdown")
async def shutdown_event():
    # Cancelar la tarea periódica
    if app.periodic_task:
        app.periodic_task.cancel()
        try:
            await app.periodic_task
        except asyncio.CancelledError:
            pass

    # Cerrar la conexión con MongoDB
    if app.mongodb_client:
        app.mongodb_client.close()


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

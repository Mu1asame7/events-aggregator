import asyncio

from fastapi import APIRouter, Depends

from app.api.dependencies import get_sync_usecase
from app.usecases.sync_events import SyncEventsUsecase

router = APIRouter()


@router.post("/sync/trigger")
async def trigger_sync(usecase: SyncEventsUsecase = Depends(get_sync_usecase)):
    asyncio.create_task(usecase.execute())

    return {"message": "Sync started"}

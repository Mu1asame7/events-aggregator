from fastapi import Depends

from app.core.config import settings
from app.core.database import AsyncSession, get_db
from app.repositories.event_repo import EventRepository
from app.repositories.place_repo import PlaceRepository
from app.repositories.sync_metadata_repo import SyncMetadataRepository
from app.services.events_provider_client import EventsProviderClient
from app.usecases.sync_events import SyncEventsUsecase


async def get_sync_usecase(db: AsyncSession = Depends(get_db)) -> SyncEventsUsecase:
    client = EventsProviderClient(
        base_url=settings.EVENTS_PROVIDER_BASE_URL,
        api_key=settings.EVENTS_PROVIDER_API_KEY,
    )

    place_repo = PlaceRepository(db)
    event_repo = EventRepository(db)
    sync_metadata_repo = SyncMetadataRepository(db)

    return SyncEventsUsecase(client, place_repo, event_repo, sync_metadata_repo)

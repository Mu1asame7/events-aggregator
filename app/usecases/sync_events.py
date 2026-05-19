from datetime import UTC, datetime

from loguru import logger

from app.repositories.event_repo import EventRepository
from app.repositories.place_repo import PlaceRepository
from app.repositories.sync_metadata_repo import SyncMetadataRepository
from app.services.events_paginator import EventsPaginator
from app.services.events_provider_client import EventsProviderClient


class SyncEventsUsecase:
    def __init__(
        self,
        client: EventsProviderClient,
        place_repo: PlaceRepository,
        event_repo: EventRepository,
        sync_metadata_repo: SyncMetadataRepository,
    ):
        self.client = client
        self.place_repo = place_repo
        self.event_repo = event_repo
        self.sync_metadata_repo = sync_metadata_repo

    async def execute(self):
        try:
            metadata = await self.sync_metadata_repo.get()
            last_changed_at = metadata.last_changed_at or "2000-01-01"

            started_at = datetime.now(UTC)

            await self.sync_metadata_repo.update(
                {
                    "status": "in_progress",
                    "last_sync_started_at": started_at,
                    "error_message": None,
                }
            )

            paginator = EventsPaginator(self.client, changed_at=last_changed_at)

            max_changed_at = None
            event_count = 0

            async for event in paginator:
                place_data = event["place"]
                place = await self.place_repo.upsert(place_data)

                await self.event_repo.upsert(event, place.id)

                event_changed_at = event["changed_at"]
                if max_changed_at is None or event_changed_at > max_changed_at:
                    max_changed_at = event_changed_at

                event_count += 1

            completed_at = datetime.now(UTC)

            await self.sync_metadata_repo.update(
                {
                    "status": "success",
                    "last_sync_completed_at": completed_at,
                    "last_changed_at": max_changed_at or last_changed_at,
                }
            )
        except Exception as e:
            await self.sync_metadata_repo.update({"status": "failed", "error_message": str(e)})

            logger.error(f"Failed: {e}")

            raise

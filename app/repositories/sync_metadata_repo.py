from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sync_metadata import SyncMetadata


class SyncMetadataRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self) -> SyncMetadata:
        result = await self._session.get(SyncMetadata, 1)

        if not result:
            result = SyncMetadata(
                id=1,
                last_changed_at="2000-01-01",
                status="success",
                last_sync_started_at=None,
                last_sync_completed_at=None,
                error_message=None,
            )
            self._session.add(result)
            await self._session.flush()

        return result

    async def update(self, data: dict) -> SyncMetadata:
        sync_meta = await self.get()

        if "last_changed_at" in data:
            sync_meta.last_changed_at = data["last_changed_at"]
        if "last_sync_completed_at" in data:
            sync_meta.last_sync_completed_at = data["last_sync_completed_at"]
        if "last_sync_started_at" in data:
            sync_meta.last_sync_started_at = data["last_sync_started_at"]
        if "status" in data:
            sync_meta.status = data["status"]
        if "error_message" in data:
            sync_meta.error_message = data["error_message"]

        await self._session.flush()

        return sync_meta

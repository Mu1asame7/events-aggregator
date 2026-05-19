from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event


class EventRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, event_id: str) -> Event | None:
        return await self._session.get(Event, event_id)

    async def upsert(self, event_data: dict, place_id: str) -> Event:
        event_id = event_data["id"]

        event = await self.get(event_id)

        if not event:
            event = Event(
                id=event_data["id"],
                name=event_data["name"],
                event_time=event_data["event_time"],
                registration_deadline=event_data["registration_deadline"],
                status=event_data["status"],
                number_of_visitors=event_data["number_of_visitors"],
                changed_at=event_data["changed_at"],
                created_at=event_data["created_at"],
                status_changed_at=event_data["status_changed_at"],
                place_id=place_id,
            )
            self._session.add(event)
        else:
            event.name = event_data["name"]
            event.event_time = event_data["event_time"]
            event.registration_deadline = event_data["registration_deadline"]
            event.status = event_data["status"]
            event.number_of_visitors = event_data["number_of_visitors"]
            event.changed_at = event_data["changed_at"]
            event.status_changed_at = event_data["status_changed_at"]

        await self._session.flush()
        return event

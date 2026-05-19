from sqlalchemy.ext.asyncio import AsyncSession
from app.models.place import Place


class PlaceRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, place_id: str) -> Place | None:
        return await self._session.get(Place, place_id)

    async def upsert(self, place_data: dict) -> Place:
        place_id = place_data["id"]
        place = await self.get(place_id)

        if not place:
            place = Place(
                id=place_id,
                name=place_data["name"],
                city=place_data["city"],
                address=place_data["address"],
                seats_pattern=place_data["seats_pattern"],
            )
            self._session.add(place)
        else:
            place.name=place_data["name"]
            place.city=place_data["city"]
            place.address=place_data["address"]
            place.seats_pattern=place_data["seats_pattern"]

        await self._session.flush()
        return place
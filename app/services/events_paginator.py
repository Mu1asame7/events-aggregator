from app.services.events_provider_client import EventsProviderClient


class EventsPaginator:
    def __init__(self, client: EventsProviderClient, changed_at: str):
        self.client = client
        self.changed_at = changed_at

        self.current_page: list[dict[str, any]] = []
        self.current_index: int = 0
        self.next_url: str | None = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.current_page:
            await self._load_next_page()
            if not self.current_page:
                raise StopAsyncIteration
            self.current_index = 0

        if self.current_index >= len(self.current_page):
            await self._load_next_page()
            if not self.current_page:
                raise StopAsyncIteration
            self.current_index = 0

        event = self.current_page[self.current_index]
        self.current_index += 1
        return event

    async def _load_next_page(self):

        result = await self.client.get_events(
            changed_at=self.changed_at,
            next_url=self.next_url,
        )

        self.current_page = result.get("results", [])
        next_url = result.get("next")
        if next_url and next_url.startswith("http://"):
            next_url = next_url.replace("http://", "https://")
        self.next_url = result.get("next")

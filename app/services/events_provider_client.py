import httpx
from loguru import logger


class EventsProviderError(Exception):
    """Базовое исключение для Events Provider API"""

    pass


class NotFoundError(EventsProviderError):
    """404 - ресурс не найден"""

    pass


class UnauthorizedError(EventsProviderError):
    """401 - неверный API ключ"""

    pass


class RateLimitError(EventsProviderError):
    """429 - слишком много запросов"""

    pass


class EventsProviderClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            headers={"x-api-key": self.api_key},
        )

    async def _request(self, method: str, endpoint: str, params=None, data=None):

        if not endpoint.endswith("/"):
            endpoint += "/"

        logger.debug(f"Request: {method} {endpoint} | params={params} | data={data}")

        if method == "GET":
            response = await self._client.request(
                method, endpoint, params=params, follow_redirects=True
            )
        elif method in ["POST", "DELETE"]:
            response = await self._client.request(
                method, endpoint, json=data, follow_redirects=True
            )
        else:
            raise ValueError(f"Unknown method: {method}")

        if response.status_code in [200, 201]:
            logger.debug(f"Response: {response.status_code} OK")
            return response.json()

        try:
            error_json = response.json()
            error_text = str(error_json)
        except ValueError:
            error_text = response.text

        logger.error(
            f"Request failed: {method} {endpoint} - {response.status_code} - {error_text}"
        )

        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {endpoint}")
        elif response.status_code == 401:
            raise UnauthorizedError("Invalid API key")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        else:
            raise EventsProviderError(f"HTTP {response.status_code}: {error_text}")

    async def get_events(self, changed_at: str = None, next_url: str = None):
        if next_url:
            response = await self._client.get(
                next_url, follow_redirects=True
            )  # ← ключевой параметр
            return response.json()
        else:
            return await self._request(
                "GET", "/api/events/", params={"changed_at": changed_at}
            )

    async def get_seats(self, event_id: str):
        endpoint = f"/api/events/{event_id}/seats/"

        return await self._request(method="GET", endpoint=endpoint)

    async def register(
        self, event_id: str, first_name: str, last_name: str, email: str, seat: str
    ):
        endpoint = f"/api/events/{event_id}/register/"

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "seat": seat,
        }

        return await self._request(method="POST", endpoint=endpoint, data=data)

    async def unregister(self, event_id: str, ticket_id: str):
        endpoint = f"/api/events/{event_id}/unregister/"

        data = {"ticket_id": ticket_id}

        return await self._request(method="DELETE", endpoint=endpoint, data=data)

    async def close(self):
        await self._client.aclose()

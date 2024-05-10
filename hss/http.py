from typing import Optional
import aiohttp

from .types import RawSchoolData, RawClassData, RawClientUserData, RawUserData
from .errors import NotFound, Forbidden, BadRequest, HTTPException


__all__ = ["HTTPClient", "BASE_URL"]


BASE_URL = "https://hss-dev.aknet.tech/v1/"


class HTTPClient:
    def __init__(self, token: str, *, session: Optional[aiohttp.ClientSession] = None):
        if session is None:
            timeout = aiohttp.ClientTimeout(10.0)
            session = aiohttp.ClientSession(timeout=timeout)
        if session.closed:
            raise ValueError("Session was already closed.")
        self.session = session
        self._token = token
        self._headers = {
            'Authorization': f"Bearer {token}"
        }

    async def request(self, endpoint):
        url = BASE_URL + endpoint
        async with self.session.get(url, headers=self._headers) as response:
            content = await response.json()
            if response.ok:
                return content
            else:
                if response.status == 404:
                    raise NotFound(response.reason)
                elif response.status == 403:
                    raise Forbidden(response.reason)
                elif response.status == 400:
                    raise BadRequest(response.reason)
                else:
                    raise HTTPException(
                        "Unknown API Error has occurred: ", response.status, response.reason
                    )

    async def get_all_schools(self) -> list[str]:
        data = await self.request("permission")
        return data["body"]["schools"]

    async def get_school(self, school_id: int) -> RawSchoolData:
        data = await self.request(f"school/{school_id}")
        return data["body"]["data"]

    async def get_school_classes(self, school_id: int) -> list[dict[str, list[int]]]:
        # このエンドポイントはdocsには書かれていない
        data = await self.request(f"school/{school_id}/class")
        return data["body"]['classes']

    async def get_class_data(self, school_id: int, grade_id: int, class_id: int) -> RawClassData:
        data = await self.request(f"school/{school_id}/userdatas/{grade_id}/{class_id}")
        return data["body"]

    async def get_client_user(self) -> RawClientUserData:
        data = await self.request(f"users/@me")
        return data["body"]["data"]

    async def get_user(self, user_id: int) -> RawUserData:
        data = await self.request(f"users/{user_id}")
        return data["body"]["data"]

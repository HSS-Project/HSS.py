from __future__ import annotations
from typing import Optional

import aiohttp

from .http import HTTPClient
from .school import School
from .user import ClientUser, User

__all__ = ["Client"]


class Client:
    "HSS Client"
    def __init__(self) -> None:
        self.is_ready: bool = False

    async def setup(
        self, token: str, *, session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self._http = HTTPClient(token, session=session)
        self._schools: dict[int, School] = {}
        self._users: dict[int, User] = {}
        self._user_id_cache: set[int] = set()

        cu_data = await self._http.get_client_user()
        self.user: ClientUser = ClientUser(
            self, int(cu_data["hid"]), cu_data["description"],
            cu_data["username"], int(cu_data["ownerId"])
        )
        self._users[self.user.id] = self.user
        self._user_id_cache.add(self.user.id)

        schools = await self._http.get_all_schools()
        for school_id in schools:
            raw_data = await self._http.get_school(int(school_id))
            school = School.from_raw_data(self, raw_data)
            self._schools[int(school_id)] = school

        self.is_ready = True

    async def reload(self) -> None:
        await self.setup(self._http._token, session=self._http.session)

    @property
    def schools(self):
        return self._schools.values()

    def get_school(self, id: int) -> Optional[School]:
        return self._schools.get(id, None)

    async def close(self):
        await self._http.session.close()

    @property
    def users(self):
        return self._users.values()

    def get_user(self, id: int) -> Optional[User]:
        return self._users.get(id, None)

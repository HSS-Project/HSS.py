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
        """Setup the client.

        Setup the client. All schools your client can see will be cached on the
        memory, but all users your client can see will NOT be cached because of
        API scheme. You can check if the client is ready by using `is_ready`. 

        Args:
            token: The HSS-API Token of your application.
            session: The `aiohttp.ClientSession` object which you can
                customize. In default, the new session with 10-second timeout
                will be used.

        Raises:
            Forbidden: The token is not valid.
            ValueError: The session was already closed.

        Note:
            This function calls the HSS-API as many times as the number of
            schools which the application can see. It is not recommended to
            call this function frequently.
        """
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

    async def fetch_schools_from_discord(self, discord_id: int) -> list[School]:
        data = await self._http.get_schools_from_discord_user(discord_id)
        ret = []
        for school_id in data["registeredSchools"]:
            school = self.get_school(int(school_id))
            if school is not None:
                ret.append(school)
        return ret

from typing import TYPE_CHECKING

from .types import SchoolType, RawSchoolData, RawClassData
from .user import User
from .classes import Class
from .errors import NotFound

if TYPE_CHECKING:
    from .client import Client

__all__ = ["School"]


class School:
    def __init__(
        self, id: int, client: "Client", owner_id: int,
        admin_ids: tuple[int, ...], name: str, type: SchoolType,
        classes_data: list[RawClassData]
    ):
        self.id = id
        self.client = client

        if owner_id in client._user_id_cache:
            self.owner: User = client.get_user(owner_id)  # type: ignore
        else:
            client._user_id_cache.add(owner_id)
            self.client._users[owner_id] = self.owner = User(client, owner_id)

        self.admins: list[User] = []
        for id in admin_ids:
            if id in client._user_id_cache:
                self.admins.append(client.get_user(id))  # type: ignore
            else:
                client._user_id_cache.add(id)
                us = self.client._users[id] = User(client, id)
                self.admins.append(us)

        self.name: str = name
        self.type: SchoolType = type
        self._classes: dict[int, dict[int, Class]] = {}
        self.setup_classes(classes_data)

    def setup_classes(self, classes: list[RawClassData]) -> None:
        for class_data in classes:
            grade = int(class_data["grade"])
            if grade not in self._classes:
                self._classes[grade] = {}
            class_number = int(class_data["class"])
            class_obj = Class.from_raw_data(self.client, self.id, class_data)
            self._classes[grade][class_number] = class_obj

    async def update_data(self) -> None:
        raw_data = await self.client._http.get_school(self.id)
        details = raw_data["details"]

        owner_id = int(details["ownerId"])
        if owner_id in self.client._user_id_cache:
            self.owner: User = client.get_user(owner_id)  # type: ignore
        else:
            self.client._user_id_cache.add(owner_id)
            self.client._users[owner_id] = self.owner = User(self.client, owner_id)

        self.admins: list[User] = []
        for i in details["admins"]:
            id = int(i)
            if id in self.client._user_id_cache:
                self.admins.append(client.get_user(id))  # type: ignore
            else:
                self.client._user_id_cache.add(id)
                us = self.client._users[id] = User(self.client, id)
                self.admins.append(us)

        self.name = details["name"]
        self.type = details["type"]
        self._classes: dict[int, dict[int, Class]] = {}
        self.setup_classes(raw_data["userDatas"])

    @classmethod
    def from_raw_data(cls, client: "Client", data: RawSchoolData):
        return cls(
            int(data["schoolId"]), client, int(data["details"]["ownerId"]),
            tuple(int(i) for i in data["details"]["admins"]),
            data["details"]["name"], data["details"]["type"], data["userDatas"]
        )

    @property
    def classes(self):
        return self._classes.values()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, School):
            return other.id == self.id
        return NotImplemented

from typing import Optional, TYPE_CHECKING
import logging

from .errors import NotFound

if TYPE_CHECKING:
    from .client import Client


class User:
    def __init__(
        self, client: "Client", id: int, developer: Optional[bool] = None,
        is_discord: Optional[bool] = None, name: Optional[str] = None,
        is_bot: Optional[bool] = None, description: Optional[str] = None
    ):
        self.id = id
        self.client = client
        self.is_partial: bool = name is None
        self.developer = developer
        self.is_discord = is_discord
        self.name = name
        self.is_bot = is_bot
        self.description = description

    async def fetch(self):
        _logger = logging.getLogger(__name__)
        if not self.is_partial:
            _logger.debug("This user is already cached.")
        try:
            data = await self.client._http.get_user(self.id)
        except NotFound:
            _logger.info("User not found, delete myself.")
            self.client._user_id_cache.discard(self.id)
            del self.client._users[self.id]
            return
        self.name = data["username"]
        self.is_discord = data["discordAccount"]
        self.is_bot = data["isBot"]
        self.developer = data["developer"]
        self.is_partial = True

    @property
    def cached(self):
        "The alias of `is_partial`, but its the opposite."
        return not self.is_partial

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return other.id == self.id
        return NotImplemented

    def __repr__(self) -> str:
        if self.is_partial:
            return f"<User id={self.id} cached=False>"
        else:
            return f"<User id={self.id} cached=True name='{self.name}' is_bot={self.is_bot}>"


class ClientUser(User):
    def __init__(self, client: "Client", id: int, description: str, name: str, owner_id: int):
        super().__init__(client, id, False, False, name, True, description)
        self.owner_id: int = owner_id

    async def fetch(self):
        data = await self.client._http.get_client_user()
        self.name = data["username"]
        self.developer = data["developer"]
        self.is_bot = data["isBot"]
        self.owner_id = int(data["ownerId"])
        self.is_partial = True

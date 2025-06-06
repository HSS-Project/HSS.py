from typing import Optional, Literal, TYPE_CHECKING
import aiohttp

from .types import (
    RawSchoolData, RawClassData, RawClientUserData,
    RawUserData, TimelineDayType,
    RawHomeworkData, DayTypeRevDict
)
from .errors import HTTPException, handle_http_error, NotSupported
import traceback

if TYPE_CHECKING:
    from .timeline import EventTime
    from datetime import datetime


__all__ = ["HTTPClient", "BASE_URL"]


BASE_URL = "https://hss-b-ds.akikaki.net/"
OLD_BASE_URL = "https://hss-ds.akikaki.net/v1/"


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
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
        }

    async def return_with_error_handler(self, response: aiohttp.ClientResponse):
        try:
            json = await response.json()
        except Exception:
            traceback.print_exc()
            json = {}
        if response.ok and "status" in json:
            if json["status"] != "success":
                raise HTTPException("Unknown API Error has occurred:", json)
            return json
        else:
            if json.get("status", "") != "error" or "message" not in json:
                raise HTTPException("Unknown API Error has occurred:", json)
            # エラーの振り分け
            handle_http_error(response.status, json["message"])
            raise NotImplementedError  # NoReturnを型チェッカーがNoneと勘違いするので仮置き

    async def get_request(self, endpoint: str):
        url = BASE_URL + endpoint
        async with self.session.get(url, headers=self._headers) as response:
            return await self.return_with_error_handler(response)

    async def patch_request(self, endpoint: str, data):
        # patchリクエストはNextバージョンには実装されていないので、旧バージョンのAPIを利用する。
        url = OLD_BASE_URL + endpoint
        reqjson = {"bodies": [data]}
        async with self.session.patch(url, headers=self._headers, json=reqjson) as response:
            return await self.return_with_error_handler(response)

    # GET methods

    async def get_all_schools(self) -> list[str]:
        data = await self.get_request("users/@me/permission")
        return data["data"]

    async def get_school(self, school_id: int) -> RawSchoolData:
        # docs上では school/:id だが、実際のエンドポイントは schools/:id (以下のschool/...系も同様)
        data = await self.get_request(f"schools/{school_id}")
        return data["data"]

    async def get_school_classes(self, school_id: int) -> dict[str, list[int]]:
        # docsにはあるものの、学年情報取得と競合してAPI側が正しく処理しない
        raise NotSupported("This endpoint is not supported due to a bug in the API.")

    async def get_grade_data(self, school_id: int, grade_id: int) -> list[RawClassData]:
        data = await self.get_request(f"schools/{school_id}/{grade_id}")
        return data["data"]

    async def get_class_data(self, school_id: int, grade_id: int, class_id: int) -> RawClassData:
        data = await self.get_request(f"schools/{school_id}/{grade_id}/{class_id}")
        return data["data"]

    async def get_client_user(self) -> RawClientUserData:
        data = await self.get_request("users/@me")
        return data["data"]

    async def get_user(self, user_id: int) -> RawUserData:
        data = await self.get_request(f"users/{user_id}")
        return data["data"]

    async def get_schools_from_discord_user(self, discord_user_id: int):
        # 現行バージョンでは廃止された。HSS.pyではv1.0で削除予定
        raise NotSupported("This endpoint was deleted from the API and not supported.")

    # PATCH methods

    async def _change_userdata(
        self, epdata: dict, reqdata: dict
    ) -> dict:
        # エンドポイントが同じpatchリクエストの処理をまとめる
        day = DayTypeRevDict[epdata["day"]]
        endpoint = f"school/{epdata['school']}/userdatas/{epdata['grade']}/{epdata['class']}/{day}"
        return await self.patch_request(endpoint, reqdata)

    async def patch_timeline(
        self, school_id: int, grade_id: int, class_id: int, day: TimelineDayType,
        state: Literal["add", "remove", "update"], name: str, place: str,
        is_event: bool, index: Optional[int] = None
    ) -> dict:
        epdata = {"school": school_id, "grade": grade_id, "class": class_id, "day": day}
        reqdata = {
            "key": "timelineData", "state": state,
            "value": {"name": name, "place": place, "IsEvent": is_event},
        }

        if index is not None:
            if state == "add":
                raise ValueError(f"Unnecessary parameter 'index' was passed on {state} mode.")
            reqdata["index"] = index

        return await self._change_userdata(epdata, reqdata)

    async def patch_default_timeline(
        self, school_id: int, grade_id: int, class_id: int, day: TimelineDayType,
        state: Literal["add", "remove", "update"], name: str, place: str,
        is_event: bool, index: Optional[int] = None
    ) -> dict:
        epdata = {"school": school_id, "grade": grade_id, "class": class_id, "day": day}
        reqdata = {
            "key": "defaultTimelineData", "state": state,
            "value": {"name": name, "place": place, "IsEvent": is_event}
        }

        if index is not None:
            if state == "add":
                raise ValueError(f"Unnecessary parameter 'index' was passed on {state} mode.")
            reqdata["index"] = index

        return await self._change_userdata(epdata, reqdata)

    async def patch_event(
        self, school_id: int, grade_id: int, class_id: int, day: TimelineDayType,
        state: Literal["add", "remove", "update"], name: str, place: str,
        time: Optional["EventTime"], index: Optional[int] = None
    ) -> dict:
        def _get_datetime(time: Optional["datetime"]) -> Optional[int]:
            if time is None:
                return None
            return int(time.timestamp())

        if state == "add":
            if time is None:
                raise ValueError("Time parameter must be passed on 'add' mode.")
            timedata = {
                "start": _get_datetime(time.start), "end": _get_datetime(time.end),
                "isEndofDay": time.is_end_of_day
            }
        else:
            timedata = {}
        epdata = {"school": school_id, "grade": grade_id, "class": class_id, "day": day}
        reqdata = {
            "key":"eventData", "state": state,
            "value":{"name": name, "place": place, "timeData": timedata}
        }

        if index is not None:
            if state == "add":
                raise ValueError(f"Unnecessary parameter 'index' was passed on {state} mode.")
            reqdata["index"] = index

        return await self._change_userdata(epdata, reqdata)

    async def patch_homework(
        self, school_id: int, grade_id: int, class_id: int,
        state: Literal["add", "remove", "update"], homework: RawHomeworkData | dict,
        index: Optional[int] = None
    ) -> dict:
        if state == "add":
            homeworkdata = homework
        else:
            homeworkdata = {}
        epdata = {"school": school_id, "grade": grade_id, "class": class_id, "day": "mon"}
        reqdata = {"key": "homework", "value": homeworkdata, "state": state}

        if index is not None:
            if state == "add":
                raise ValueError(f"Unnecessary parameter 'index' was passed on {state} mode.")
            reqdata["index"] = index

        return await self._change_userdata(epdata, reqdata)

    async def patch_default_timeline_index(
        self, school_id: int, grade_id: int, class_id: int,
        new_index: int
    ) -> dict:
        epdata = {"school": school_id, "grade": grade_id, "class": class_id, "day": "mon"}
        reqdata = {"key": "defaultTimelineIndex", "value": new_index, "state": "update"}
        return await self._change_userdata(epdata, reqdata)


from enum import Enum
from typing import TypedDict, Literal


class SchoolType(Enum):
    Kosen = 0
    NormalSchool = 1
    InternetSchool = 2
    BetaSchool = 3  # ベータ版でのみ作成できる学校の種別


class RawTimelineClassData(TypedDict):
    name: str
    place: str
    IsEvent: bool


class RawTimelineData(TypedDict):
    sun: list[RawTimelineClassData]
    mon: list[RawTimelineClassData]
    tue: list[RawTimelineClassData]
    wed: list[RawTimelineClassData]
    thu: list[RawTimelineClassData]
    fri: list[RawTimelineClassData]
    sat: list[RawTimelineClassData]


class RawTimeData(TypedDict):
    start: int | None  # 1970年1月1日からの経過ミリ秒
    end: int | None  # 上同
    is_end_of_day: bool


class RawEventData(RawTimelineData):
    name: str
    place: str
    timeData: RawTimeData


RawClassData = TypedDict(
    "RawClassData",
    {
        "defaultTimelineIndex": int,
        "grade": int, "class": int, "homework": list,
        "timelineData": RawTimelineData,
        "eventData": RawEventData,
        "defaultTimelineData": RawTimelineData
    }
)  # キー`class`(予約語で使用不可)が存在するためここだけ別形式


class TimelineDayType(Enum):
    sun = 0
    mon = 1
    tue = 2
    wed = 3
    thu = 4
    fri = 5
    sat = 6


class RawSchoolDetailData(TypedDict):
    type: SchoolType
    name: str
    id: str
    ownerId: str
    admins: list[str]
    timelineDefaultIndexs: int  # このキーはdocsには明記されていない


class RawSchoolData(TypedDict):
    schoolId: str
    details: RawSchoolDetailData
    userDatas: list[RawClassData]


class RawClientUserData(TypedDict):
    hid: str
    username: str
    developer: Literal[False]
    isBot: Literal[True]
    description: str
    ownerId: str  # このキーはdocsには明記されていない


class RawUserData(TypedDict):
    hid: str
    username: str
    developer: bool
    discordAccount: bool
    isBot: bool


class RawSchoolsFromDiscordData(TypedDict):
    discordUserId: str
    registeredSchools: list[str]


class RawHomeworkPageData(TypedDict):
    start: str | int
    end: str | int
    comment: str | None


class RawHomeworkData(TypedDict):
    name: str
    istooBig: bool
    page: RawHomeworkPageData

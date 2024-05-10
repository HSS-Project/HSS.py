from enum import Enum
from typing import TypedDict, Literal


class SchoolType(Enum):
    Kosen = 0
    NormalSchool = 1
    InternetSchool = 2
    BetaSchool = 3  # This type used only at beta version.


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


class RawEventData(RawTimelineData):
    pass  # 現時点で、このデータにはTimelineDataとの差異はない


RawClassData = TypedDict(
    "RawClassData",
    {
        "defaultTimelineIndex": int,
        "grade": int, "class": int, "homework": list,
        "timelineData": RawTimelineData,
        "eventData": RawEventData,
        "defaultTimelineData": RawTimelineData
    }
)


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
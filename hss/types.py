from enum import Enum
from typing import TypedDict, Literal, NotRequired


class SchoolType(Enum):
    Kosen = 0
    NormalSchool = 1
    InternetSchool = 2
    BetaSchool = 3  # ベータ版でのみ作成できる学校の種別


class RawLessonData(TypedDict):
    # タイムライン上の各データには名前がついていないため、仮に「Lesson」と命名
    name: str
    place: str
    IsEvent: bool


class RawTimelineData(TypedDict):
    sun: list[RawLessonData]
    mon: list[RawLessonData]
    tue: list[RawLessonData]
    wed: list[RawLessonData]
    thu: list[RawLessonData]
    fri: list[RawLessonData]
    sat: list[RawLessonData]


class RawTimeData(TypedDict):
    start: int | None  # 1970年1月1日からの経過ミリ秒
    end: int | None  # 上同
    isEndofDay: bool


class RawEventData(RawLessonData):
    name: str
    place: str
    timeData: RawTimeData


class RawEventTimelineData(TypedDict):
    sun: list[RawEventData]
    mon: list[RawEventData]
    tue: list[RawEventData]
    wed: list[RawEventData]
    thu: list[RawEventData]
    fri: list[RawEventData]
    sat: list[RawEventData]


RawClassData = TypedDict(
    "RawClassData",
    {
        "defaultTimelineIndex": int,
        "grade": int, "class": int, "homework": list,
        "timelineData": RawTimelineData,
        "eventData": RawEventTimelineData,
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
    isBot: Literal[True]  # このキーはdocsには明記されていない
    description: str  # このキーはdocsには明記されていない
    ownerId: str  # このキーはdocsには明記されていない
    # email: str  # このキーはdocsにあるが実際にはない
    # discordAccount: NotRequired[bool]  # このキーはdocsにあるが実際にはない


class RawUserData(TypedDict):
    hid: str
    username: str
    developer: bool
    discordAccount: NotRequired[bool]
    isBot: bool  # docs上ではNotRequired[bool]だが、必ずある
    description: NotRequired[bool]


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


DayTypeDict: dict[str, TimelineDayType] = {
    "sun": TimelineDayType.sun,
    "mon": TimelineDayType.mon,
    "tue": TimelineDayType.tue,
    "wed": TimelineDayType.wed,
    "thu": TimelineDayType.thu,
    "fri": TimelineDayType.fri,
    "sat": TimelineDayType.sat,
}

DayTypeRevDict: dict[TimelineDayType, str] = {
    TimelineDayType.sun: "sun",
    TimelineDayType.mon: "mon",
    TimelineDayType.tue: "tue",
    TimelineDayType.wed: "wed",
    TimelineDayType.thu: "thu",
    TimelineDayType.fri: "fri",
    TimelineDayType.sat: "sat",
}

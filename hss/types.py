from enum import Enum
from typing import TypedDict, Literal, NotRequired


__ALL__ = [
    "SchoolType",
    "TimelineDayType",
    "DayTypeDict",
    "DayTypeRevDict",
]


class SchoolType(Enum):
    Kosen = 0
    NormalSchool = 1
    InternetSchool = 2
    BetaSchool = 3  # ベータ版でのみ作成できる学校の種別


RawLessonData = TypedDict(
    "RawLessonData",
    {
        "name": str,
        "place": str,
        "IsEvent": bool,
    }
)  # タイムライン上の各データには名前がついていないため、仮に「Lesson」と命名


RawTimelineData = TypedDict(
    "RawTimelineData",
    {
        "sun": list[RawLessonData],
        "mon": list[RawLessonData],
        "tue": list[RawLessonData],
        "wed": list[RawLessonData],
        "thu": list[RawLessonData],
        "fri": list[RawLessonData],
        "sat": list[RawLessonData]
    }
)


RawTimeData = TypedDict(
    "RawTimeData",
    {
        "start": int | None,  # 1970年1月1日からの経過ミリ秒
        "end": int | None,  # 上同
        "isEndofDay": bool,
    }
)


RawEventData = TypedDict(
    "RawEventData",
    {
        "name": str,
        "place": str,
        "IsEvent": bool,
        "timeData": RawTimeData,
    }
)


RawEventTimelineData = TypedDict(
    "RawEventTimelineData",
    {
        "sun": list[RawTimeData],
        "mon": list[RawTimeData],
        "tue": list[RawTimeData],
        "wed": list[RawTimeData],
        "thu": list[RawTimeData],
        "fri": list[RawTimeData],
        "sat": list[RawTimeData]
    }
)


RawClassData = TypedDict(
    "RawClassData",
    {
        "defaultTimelineIndex": int,
        "grade": int, "class": int, "homework": list,
        "timelineData": RawTimelineData,
        "eventData": RawEventTimelineData,
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


RawSchoolDetailData = TypedDict(
    "RawSchoolDetailData",
    {
        "type": SchoolType,
        "name": str,
        "id": str,
        "ownerId": str,
        "admins": list[str],
        "timelineDefaultIndexs": int,  # このキーはdocsには明記されていない
    }
)


RawSchoolData = TypedDict(
    "RawSchoolData",
    {
        "schoolId": str,
        "details": RawSchoolDetailData,
        "userDatas": list[RawClassData],
    }
)


RawClientUserData = TypedDict(
    "RawClientUserData",
    {
        "hid": str,
        "username": str,
        "developer": Literal[False],
        "isBot": Literal[True],  # このキーはdocsには明記されていない
        "description": str,  # このキーはdocsには明記されていない
        "ownerId": str,  # このキーはdocsには明記されていない
        # "email": str,  # このキーはdocsにあるが実際にはない
        # "discordAccount": NotRequired[bool]  # このキーはdocsにあるが実際にはない
    }
)


RawUserData = TypedDict(
    "RawUserData",
    {
        "hid": str,
        "username": str,
        "developer": bool,
        "discordAccount": NotRequired[bool],
        "isBot": bool,  # docs上ではNotRequired[bool]だが、必ずある
        "description": NotRequired[bool]
    }
)


RawHomeworkPageData = TypedDict(
    "RawHomeworkPageData",
    {
        "start": str | int,
        "end": str | int,
        "comment": str | None,
    }
)


RawHomeworkData = TypedDict(
    "RawHomeworkData",
    {
        "name": str,
        "istooBig": bool,
        "page": RawHomeworkPageData,
    }
)


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

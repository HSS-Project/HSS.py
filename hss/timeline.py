from typing import TYPE_CHECKING

from .types import TimelineDayType, RawTimelineData, RawTimelineClassData

if TYPE_CHECKING:
    from .client import Client


__all__ = ["Lesson", "DayTimeline", "Timeline"]


DayTypeDict: dict[str, TimelineDayType] = {
    "sun": TimelineDayType.sun,
    "mon": TimelineDayType.mon,
    "tue": TimelineDayType.tue,
    "wed": TimelineDayType.wed,
    "thu": TimelineDayType.thu,
    "fri": TimelineDayType.fri,
    "sat": TimelineDayType.sat,
}


class Lesson:
    def __init__(self, name: str, place: str, is_event: bool):
        self.name = name
        self.place = place
        self.is_event = is_event


class DayTimeline:
    def __init__(self, client: "Client", day: TimelineDayType, lessons: list[Lesson]):
        self.client = client
        self.day = day
        self.lessons = lessons

    @classmethod
    def from_raw_data(
        cls, client: "Client", day: TimelineDayType, data: list[RawTimelineClassData]
    ):
        lessons = []
        for cl in data:
            lessons.append(Lesson(cl["name"], cl["place"], cl["IsEvent"]))
        return cls(client, day, lessons)


class Timeline:
    def __init__(
        self, client: "Client", sunday: DayTimeline, monday: DayTimeline,
        tuesday: DayTimeline, wednesday: DayTimeline, thursday: DayTimeline,
        friday: DayTimeline, saturday: DayTimeline
    ):
        self.client = client
        self.sunday = self.sun = sunday
        self.monday = self.mon = monday
        self.tuesday = self.tue = tuesday
        self.wednesday = self.wed = wednesday
        self.thursday = self.thu = thursday
        self.friday = self.fri = friday
        self.saturday = self.sat = saturday

    @classmethod
    def from_raw_data(cls, client: "Client", data: RawTimelineData):
        args: list[DayTimeline] = []
        for day in data.keys():
            day_enum = DayTypeDict[day]
            day_time_line = DayTimeline.from_raw_data(client, day_enum, data[day])
            args.append(day_time_line)
        if len(args) != 7:
            raise ValueError(f"API returned data with only {len(args)} days.")
        return cls(client, *args)

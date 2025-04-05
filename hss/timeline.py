from typing import TYPE_CHECKING, Optional
from collections.abc import Sequence

from datetime import datetime

from .types import (
    TimelineDayType, RawTimelineData, RawLessonData, RawEventTimelineData,
    RawEventData, RawTimeData, DayTypeDict, DayTypeRevDict
)

if TYPE_CHECKING:
    from .client import Client
    from .classes import Class


__all__ = ["Lesson", "DayTimeline", "Timeline"]

class Lesson:
    def __init__(self, name: str, place: str, is_event: bool):
        self.name = name
        self.place = place
        self.is_event = is_event
    
    def __repr__(self) -> str:
        return f"<Lesson name='{self.name}' place='{self.place}' is_event={self.is_event}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Lesson):
            return (other.name == self.name and other.place == self.place
                    and other.is_event == self.is_event)
        raise NotImplementedError

    def copy(self) -> "Lesson":
        return Lesson(self.name, self.place, self.is_event)



class DayTimeline:
    def __init__(
        self, client: "Client", day: TimelineDayType,
        lessons: Sequence[Optional[Lesson]]
    ):
        self.client = client
        self.day = day
        self.lessons = list(lessons)

    @classmethod
    def from_raw_data(
        cls, client: "Client", day: TimelineDayType, data: list[RawLessonData],
    ):
        lessons: list[Optional[Lesson]] = []
        for cl in data:
            if cl is None:
                lessons.append(None)
            else:
                lessons.append(Lesson(cl["name"], cl["place"], cl["IsEvent"]))
        return cls(client, day, lessons)

    def __len__(self):
        return len(self.lessons)

    def __repr__(self) -> str:
        return f"<DayTimeline len={self.__len__()}>"

    def copy(self) -> "DayTimeline":
        new_lessons = []
        for i in self.lessons:
            if i:
                new_lessons.append(i.copy())
            else:
                new_lessons.append(i)
        return DayTimeline(self.client, self.day, new_lessons)


class Timeline:
    def __init__(
        self, client: "Client", default: bool, sunday: DayTimeline, monday: DayTimeline,
        tuesday: DayTimeline, wednesday: DayTimeline, thursday: DayTimeline,
        friday: DayTimeline, saturday: DayTimeline
    ):
        self.client = client
        self.default = default
        self.class_: Optional["Class"] = None
        self.sun = sunday
        self.mon = monday
        self.tue = tuesday
        self.wed = wednesday
        self.thu = thursday
        self.fri = friday
        self.sat = saturday

    @property
    def sunday(self):
        return self.sun

    @property
    def monday(self):
        return self.mon

    @property
    def tuesday(self):
        return self.tue

    @property
    def wednesday(self):
        return self.wed

    @property
    def thursday(self):
        return self.thu

    @property
    def friday(self):
        return self.fri

    @property
    def saturday(self):
        return self.sat

    @classmethod
    def from_raw_data(cls, client: "Client", data: RawTimelineData, default: bool):
        args: list[DayTimeline] = []
        for day in data.keys():
            day_enum = DayTypeDict[day]
            day_time_line = DayTimeline.from_raw_data(client, day_enum, data[day])
            args.append(day_time_line)
        if len(args) != 7:
            raise ValueError(f"API returned data with only {len(args)} days.")
        return cls(client, default, *args)

    def __repr__(self) -> str:
        t = []
        for day in DayTypeDict.keys():
            t.append(f"{day}={getattr(self, day)}")
        return f"<Timeline {' '.join(t)}>"

    async def edit(self, day: TimelineDayType, timeline: DayTimeline):
        if self.class_ is None:
            raise AttributeError("The `class_` attribute must set to edit.")

        before: DayTimeline = getattr(self, DayTypeRevDict[day])
        if self.default:
            patch = self.client._http.patch_default_timeline
        else:
            patch = self.client._http.patch_timeline

        for i in range(min(len(before), len(timeline))):
            new_lesson = timeline.lessons[i]
            old_lesson = before.lessons[i]
            if new_lesson is None and old_lesson is not None:
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "remove", "", "", False, i
                )
            elif new_lesson is not None and old_lesson != new_lesson:
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "update", new_lesson.name,
                    new_lesson.place, new_lesson.is_event, i
                )

        if len(before) > len(timeline):
            for i in range(len(timeline), len(before)):
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "remove", "", "", False, i
                )
        elif len(before) < len(timeline):
            for i in range(len(before), len(timeline)):
                if timeline.lessons[i] is None:
                    continue
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "add", timeline.lessons[i].name,  # type: ignore
                    timeline.lessons[i].place, timeline.lessons[i].is_event  # type: ignore
                )

        setattr(self, DayTypeRevDict[day], timeline)



class EventTime:
    def __init__(
        self, start: Optional[int], end: Optional[int], is_end_of_day: bool
    ) -> None:
        if start is None:
            self.start = None
        else:
            self.start = datetime.fromtimestamp(start)
        if end is None:
            self.end = None
        else:
            self.end = datetime.fromtimestamp(end)
        self.is_end_of_day = is_end_of_day

    def __repr__(self) -> str:
        return f"<EventTime start={self.start} end={self.end} is_end_of_day={self.is_end_of_day}>"

    @classmethod
    def from_raw_data(cls, data: RawTimeData) -> "EventTime":
        if data["start"] is None:
            start = None
        else:
            start = int(data["start"])
        if data["end"] is None:
            end = None
        else:
            end = int(data["end"])
        return cls(start, end, data["isEndofDay"])

    def copy(self) -> "EventTime":
        if self.start:
            start = int(self.start.timestamp())
        else:
            start = None
        if self.end:
            end = int(self.end.timestamp())
        else:
            end = None
        return EventTime(start, end, self.is_end_of_day)


class Event(Lesson):
    def __init__(self, name: str, place: str, time: EventTime):
        super().__init__(name, place, True)
        self.time = time
    
    def copy(self) -> "Event":
        return Event(self.name, self.place, self.time.copy())

    def __repr__(self) -> str:
        return f"<Event name={self.name} place={self.place} time={self.time}>"


class DayEventTimeline(DayTimeline):
    def __init__(
        self, client: "Client", day: TimelineDayType, events: list[Optional[Event]]
    ):
        super().__init__(client, day, events)
        self.events = events

    @classmethod
    def from_raw_data(
        cls, client: "Client", day: TimelineDayType, data: list[RawEventData],
    ):
        events: list[Optional[Event]] = []
        for cl in data:
            if cl is None:
                events.append(None)
            else:
                events.append(
                    Event(cl["name"], cl["place"], EventTime.from_raw_data(cl["timeData"]))
                )
        return cls(client, day, events)

    def __len__(self):
        return len(self.events)

    def copy(self) -> "DayEventTimeline":
        new_events = []
        for i in self.events:
            if i:
                new_events.append(i.copy())
            else:
                new_events.append(i)
        return DayEventTimeline(self.client, self.day, new_events)

    def __repr__(self) -> str:
        return f"<DayEventTimeline len={len(self.events)}>"


class EventTimeline(Timeline):
    mon: DayEventTimeline
    tue: DayEventTimeline
    wed: DayEventTimeline
    thu: DayEventTimeline
    fri: DayEventTimeline
    sat: DayEventTimeline
    sun: DayEventTimeline
    monday: DayEventTimeline
    tuesday: DayEventTimeline
    wednesday: DayEventTimeline
    thursday: DayEventTimeline
    friday: DayEventTimeline
    saturday: DayEventTimeline
    sunday: DayEventTimeline

    def __init__(
        self, client: "Client", sunday: DayEventTimeline, monday: DayEventTimeline,
        tuesday: DayEventTimeline, wednesday: DayEventTimeline, thursday: DayEventTimeline,
        friday: DayEventTimeline, saturday: DayEventTimeline
    ):
        super().__init__(
            client, False, sunday, monday, tuesday, 
            wednesday, thursday, friday, saturday
        )

    @classmethod
    def from_raw_data(cls, client: "Client", data: RawEventTimelineData):
        args: list[DayEventTimeline] = []
        for day in data.keys():
            day_enum = DayTypeDict[day]
            day_time_line = DayEventTimeline.from_raw_data(client, day_enum, data[day])
            args.append(day_time_line)
        if len(args) != 7:
            raise ValueError(f"API returned data with only {len(args)} days.")
        return cls(client, *args)

    def __repr__(self) -> str:
        t = []
        for day in DayTypeDict.keys():
            t.append(f"{day}={getattr(self, day)}")
        return f"<EventTimeline {' '.join(t)}>"

    async def edit(self, day: TimelineDayType, timeline: DayEventTimeline):
        if self.class_ is None:
            raise AttributeError("The `class_` attribute must set to edit.")

        before: DayEventTimeline = getattr(self, DayTypeRevDict[day])
        patch = self.client._http.patch_event

        for i in range(min(len(before), len(timeline))):
            new_lesson = timeline.events[i]
            old_lesson = before.events[i]
            if new_lesson is None and old_lesson is not None:
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "remove", "", "", None, i
                )
            elif new_lesson is not None and old_lesson != new_lesson:
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "update", new_lesson.name,
                    new_lesson.place, new_lesson.time, i
                )

        if len(before) > len(timeline):
            for i in range(len(timeline), len(before)):
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "remove", "", "", None, i
                )
        elif len(before) < len(timeline):
            for i in range(len(before), len(timeline)):
                if timeline.events[i] is None:
                    continue
                await patch(
                    self.class_.school_id, self.class_.grade,
                    self.class_.class_, day, "add", timeline.events[i].name,  # type: ignore
                    timeline.events[i].place, timeline.events[i].time  # type: ignore
                )

        setattr(self, DayTypeRevDict[day], timeline)


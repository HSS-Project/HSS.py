from typing import TYPE_CHECKING

from .timeline import Timeline, EventTimeline
from .types import RawClassData

if TYPE_CHECKING:
    from .client import Client


class Class:
    def __init__(
        self, client: "Client", school_id: int, grade_id: int, class_id: int,
        default_timeline_index: int, homework: list, timeline: Timeline,
        event: EventTimeline, default_timeline: Timeline
    ):
        self.client = client
        self.school_id = school_id
        self.grade = grade_id
        self.class_ = class_id
        self.default_timeline_index = default_timeline_index
        self.homework = homework
        self.timeline = timeline
        self.event = event
        self.default_timeline = default_timeline
        # set self to class_
        self.event.class_ = self
        self.timeline.class_ = self
        self.default_timeline.class_ = self

    @classmethod
    def from_raw_data(cls, client: "Client", school_id: int, raw_data: RawClassData):
        timeline = Timeline.from_raw_data(client, raw_data["timelineData"], False)
        event = EventTimeline.from_raw_data(client, raw_data["eventData"])
        default_timeline = Timeline.from_raw_data(client, raw_data["defaultTimelineData"], True)
        return cls(
            client, school_id, int(raw_data["grade"]), int(raw_data["class"]),
            raw_data["defaultTimelineIndex"], raw_data["homework"],
            timeline, event, default_timeline
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Class):
            return other.grade == self.grade and other.class_ == self.class_
        return NotImplemented

    def __repr__(self) -> str:
        return f"<Class school_id={self.school_id} grade={self.grade} class_={self.class_}>"

    async def edit_default_timeline_index(self, new_index: int) -> None:
        await self.client._http.patch_default_timeline_index(
            self.school_id, self.grade, self.class_, new_index
        )

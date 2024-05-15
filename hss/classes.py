from typing import TYPE_CHECKING

from .timeline import Timeline
from .types import RawClassData

if TYPE_CHECKING:
    from .client import Client


class Class:
    def __init__(
        self, client: "Client", school_id: int, grade_id: int, class_id: int,
        default_timeline_index: int, homework: list, timeline: Timeline,
        event: Timeline, default_timeline: Timeline
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

    @classmethod
    def from_raw_data(cls, client: "Client", school_id: int, raw_data: RawClassData):
        timeline = Timeline.from_raw_data(client, raw_data["timelineData"])
        event = Timeline.from_raw_data(client, raw_data["eventData"])
        default_timeline = Timeline.from_raw_data(client, raw_data["defaultTimelineData"])
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

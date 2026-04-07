"""Events fired by the Rerun block."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from gradio import EventData
from rerun._event import (
    PauseEvent,
    PlayEvent,
    SelectionChangeEvent,
    TimelineChangeEvent,
    TimeUpdateEvent,
    _viewer_event_from_json_str,
)


class Play(EventData):
    """
    Event triggered when playback starts.

    Args:
        EventData (EventData): The base event data.

    """

    def __init__(self, target: Any, data: Any):
        """
        Initialize a Play event.

        Args:
            target (Any): The object that triggered the play event.
            data (Any): The play event data.

        """
        super().__init__(target, data)

        event = _viewer_event_from_json_str(data)
        assert event.type == "play"
        self.payload: PlayEvent = event


class Pause(EventData):
    """
    Event triggered when playback is paused.

    Args:
        EventData (EventData): The base event data.

    """

    def __init__(self, target: Any, data: Any):
        """
        Initialize a Pause event.

        Args:
            target (Any): The object that triggered the pause event.
            data (Any): The pause event data.

        """
        super().__init__(target, data)

        event = _viewer_event_from_json_str(data)
        assert event.type == "pause"
        self.payload: PauseEvent = event


class TimeUpdate(EventData):
    """Event triggered when the time is updated in the viewer."""

    def __init__(self, target: Any, data: Any) -> None:
        """
        Initialize a TimeUpdate event.

        Args:
            target (Any): The object that triggered the time update event.
            data (Any): The new time value.

        """
        super().__init__(target, data)

        event = _viewer_event_from_json_str(data)
        assert event.type == "time_update"
        self.payload: TimeUpdateEvent = event


class TimelineChange(EventData):
    """Event triggered when the timeline changes in the viewer."""

    def __init__(self, target: Any, data: Any) -> None:
        """
        Initialize a TimelineChange event.

        Args:
            target (Any): The object that triggered the timeline change event.
            data (Any): A dictionary containing timeline and time information.

        """
        super().__init__(target, data)

        event = _viewer_event_from_json_str(data)
        assert event.type == "timeline_change"
        self.payload: TimelineChangeEvent = event


class SelectionChange(EventData):
    """
    Event triggered when the selection changes in the Viewer.

    Args:
        EventData (EventData): The base event data.

    """

    def __init__(self, target: Any, data: Any):
        """
        Initialize a SelectionChange event.

        Args:
            target (Any): The object that triggered the selection change event.
            data (Any): The selection change event data.

        """
        super().__init__(target, data)

        event = _viewer_event_from_json_str(data)
        assert event.type == "selection_change"
        self.payload: SelectionChangeEvent = event


@dataclass
class TimeSelectionPayload:
    """Payload for the time_selection_change event."""

    min: float | None
    """The minimum time of the selection range, or None if no selection."""

    max: float | None
    """The maximum time of the selection range, or None if no selection."""


class TimeSelectionChange(EventData):
    """Event triggered when the time selection (loop region) changes on the timeline."""

    def __init__(self, target: Any, data: Any) -> None:
        super().__init__(target, data)

        parsed = json.loads(data) if isinstance(data, str) else data
        self.payload: TimeSelectionPayload = TimeSelectionPayload(
            min=parsed.get("min"),
            max=parsed.get("max"),
        )

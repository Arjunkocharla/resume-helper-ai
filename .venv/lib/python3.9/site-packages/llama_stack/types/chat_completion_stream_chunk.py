# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .shared.tool_call import ToolCall

__all__ = [
    "ChatCompletionStreamChunk",
    "Event",
    "EventDelta",
    "EventDeltaToolCallDelta",
    "EventDeltaToolCallDeltaContent",
    "EventLogprob",
]

EventDeltaToolCallDeltaContent: TypeAlias = Union[str, ToolCall]


class EventDeltaToolCallDelta(BaseModel):
    content: EventDeltaToolCallDeltaContent

    parse_status: Literal["started", "in_progress", "failure", "success"]


EventDelta: TypeAlias = Union[str, EventDeltaToolCallDelta]


class EventLogprob(BaseModel):
    logprobs_by_token: Dict[str, float]


class Event(BaseModel):
    delta: EventDelta

    event_type: Literal["start", "complete", "progress"]

    logprobs: Optional[List[EventLogprob]] = None

    stop_reason: Optional[Literal["end_of_turn", "end_of_message", "out_of_tokens"]] = None


class ChatCompletionStreamChunk(BaseModel):
    event: Event

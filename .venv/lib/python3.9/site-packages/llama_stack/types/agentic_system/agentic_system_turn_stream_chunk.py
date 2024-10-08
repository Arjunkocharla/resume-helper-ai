# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from ..._models import BaseModel
from .turn_stream_event import TurnStreamEvent

__all__ = ["AgenticSystemTurnStreamChunk"]


class AgenticSystemTurnStreamChunk(BaseModel):
    event: TurnStreamEvent

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompletionStreamChunk", "Logprob"]


class Logprob(BaseModel):
    logprobs_by_token: Dict[str, float]


class CompletionStreamChunk(BaseModel):
    delta: str

    logprobs: Optional[List[Logprob]] = None

    stop_reason: Optional[Literal["end_of_turn", "end_of_message", "out_of_tokens"]] = None

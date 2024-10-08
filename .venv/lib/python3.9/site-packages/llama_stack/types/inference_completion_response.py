# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel
from .completion_stream_chunk import CompletionStreamChunk
from .shared.completion_message import CompletionMessage

__all__ = ["InferenceCompletionResponse", "CompletionResponse", "CompletionResponseLogprob"]


class CompletionResponseLogprob(BaseModel):
    logprobs_by_token: Dict[str, float]


class CompletionResponse(BaseModel):
    completion_message: CompletionMessage

    logprobs: Optional[List[CompletionResponseLogprob]] = None


InferenceCompletionResponse: TypeAlias = Union[CompletionResponse, CompletionStreamChunk]

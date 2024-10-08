# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel
from .shared.completion_message import CompletionMessage
from .chat_completion_stream_chunk import ChatCompletionStreamChunk

__all__ = ["InferenceChatCompletionResponse", "ChatCompletionResponse", "ChatCompletionResponseLogprob"]


class ChatCompletionResponseLogprob(BaseModel):
    logprobs_by_token: Dict[str, float]


class ChatCompletionResponse(BaseModel):
    completion_message: CompletionMessage

    logprobs: Optional[List[ChatCompletionResponseLogprob]] = None


InferenceChatCompletionResponse: TypeAlias = Union[ChatCompletionResponse, ChatCompletionStreamChunk]

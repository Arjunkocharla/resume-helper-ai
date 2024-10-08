# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal

from ..._models import BaseModel
from .tool_call import ToolCall

__all__ = ["CompletionMessage"]


class CompletionMessage(BaseModel):
    content: Union[str, List[str]]

    role: Literal["assistant"]

    stop_reason: Literal["end_of_turn", "end_of_message", "out_of_tokens"]

    tool_calls: List[ToolCall]

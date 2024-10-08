# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..shared_params.attachment import Attachment
from ..shared_params.user_message import UserMessage
from ..shared_params.tool_response_message import ToolResponseMessage

__all__ = ["TurnCreateParamsBase", "Message", "TurnCreateParamsNonStreaming", "TurnCreateParamsStreaming"]


class TurnCreateParamsBase(TypedDict, total=False):
    agent_id: Required[str]

    messages: Required[Iterable[Message]]

    session_id: Required[str]

    attachments: Iterable[Attachment]


Message: TypeAlias = Union[UserMessage, ToolResponseMessage]


class TurnCreateParamsNonStreaming(TurnCreateParamsBase, total=False):
    stream: Literal[False]


class TurnCreateParamsStreaming(TurnCreateParamsBase):
    stream: Required[Literal[True]]


TurnCreateParams = Union[TurnCreateParamsNonStreaming, TurnCreateParamsStreaming]

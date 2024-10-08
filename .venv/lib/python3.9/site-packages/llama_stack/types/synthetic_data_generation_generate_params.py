# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shared_params.user_message import UserMessage
from .shared_params.system_message import SystemMessage
from .shared_params.completion_message import CompletionMessage
from .shared_params.tool_response_message import ToolResponseMessage

__all__ = ["SyntheticDataGenerationGenerateParams", "Dialog"]


class SyntheticDataGenerationGenerateParams(TypedDict, total=False):
    dialogs: Required[Iterable[Dialog]]

    filtering_function: Required[Literal["none", "random", "top_k", "top_p", "top_k_top_p", "sigmoid"]]

    model: str


Dialog: TypeAlias = Union[UserMessage, SystemMessage, ToolResponseMessage, CompletionMessage]

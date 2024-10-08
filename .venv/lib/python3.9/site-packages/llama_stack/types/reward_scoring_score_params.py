# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .shared_params.user_message import UserMessage
from .shared_params.system_message import SystemMessage
from .shared_params.completion_message import CompletionMessage
from .shared_params.tool_response_message import ToolResponseMessage

__all__ = [
    "RewardScoringScoreParams",
    "DialogGeneration",
    "DialogGenerationDialog",
    "DialogGenerationSampledGeneration",
]


class RewardScoringScoreParams(TypedDict, total=False):
    dialog_generations: Required[Iterable[DialogGeneration]]

    model: Required[str]


DialogGenerationDialog: TypeAlias = Union[UserMessage, SystemMessage, ToolResponseMessage, CompletionMessage]

DialogGenerationSampledGeneration: TypeAlias = Union[UserMessage, SystemMessage, ToolResponseMessage, CompletionMessage]


class DialogGeneration(TypedDict, total=False):
    dialog: Required[Iterable[DialogGenerationDialog]]

    sampled_generations: Required[Iterable[DialogGenerationSampledGeneration]]

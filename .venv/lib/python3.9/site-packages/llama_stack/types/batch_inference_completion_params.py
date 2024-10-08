# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Required, TypedDict

from .shared_params.sampling_params import SamplingParams

__all__ = ["BatchInferenceCompletionParams", "Logprobs"]


class BatchInferenceCompletionParams(TypedDict, total=False):
    content_batch: Required[List[Union[str, List[str]]]]

    model: Required[str]

    logprobs: Logprobs

    sampling_params: SamplingParams


class Logprobs(TypedDict, total=False):
    top_k: int

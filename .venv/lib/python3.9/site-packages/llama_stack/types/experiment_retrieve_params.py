# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ExperimentRetrieveParams"]


class ExperimentRetrieveParams(TypedDict, total=False):
    experiment_id: Required[str]

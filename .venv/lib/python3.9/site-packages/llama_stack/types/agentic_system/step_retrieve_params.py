# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["StepRetrieveParams"]


class StepRetrieveParams(TypedDict, total=False):
    agent_id: Required[str]

    step_id: Required[str]

    turn_id: Required[str]

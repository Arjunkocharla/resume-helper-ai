# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["DocumentRetrieveParams"]


class DocumentRetrieveParams(TypedDict, total=False):
    bank_id: Required[str]

    document_ids: Required[List[str]]

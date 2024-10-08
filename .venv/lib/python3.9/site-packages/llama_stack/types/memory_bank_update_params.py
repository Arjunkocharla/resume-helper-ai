# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["MemoryBankUpdateParams", "Document"]


class MemoryBankUpdateParams(TypedDict, total=False):
    bank_id: Required[str]

    documents: Required[Iterable[Document]]


class Document(TypedDict, total=False):
    content: Required[Union[str, List[str]]]

    document_id: Required[str]

    metadata: Required[Dict[str, Union[bool, float, str, Iterable[object], object, None]]]

    mime_type: Required[str]

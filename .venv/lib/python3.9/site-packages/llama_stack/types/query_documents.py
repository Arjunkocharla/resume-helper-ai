# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union

from .._models import BaseModel

__all__ = ["QueryDocuments", "Chunk"]


class Chunk(BaseModel):
    content: Union[str, List[str]]

    document_id: str

    token_count: int


class QueryDocuments(BaseModel):
    chunks: List[Chunk]

    scores: List[float]

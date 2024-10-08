# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable

import httpx

from ...types import (
    memory_bank_drop_params,
    memory_bank_query_params,
    memory_bank_create_params,
    memory_bank_insert_params,
    memory_bank_update_params,
    memory_bank_retrieve_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .documents import (
    DocumentsResource,
    AsyncDocumentsResource,
    DocumentsResourceWithRawResponse,
    AsyncDocumentsResourceWithRawResponse,
    DocumentsResourceWithStreamingResponse,
    AsyncDocumentsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.query_documents import QueryDocuments

__all__ = ["MemoryBanksResource", "AsyncMemoryBanksResource"]


class MemoryBanksResource(SyncAPIResource):
    @cached_property
    def documents(self) -> DocumentsResource:
        return DocumentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> MemoryBanksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return MemoryBanksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemoryBanksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return MemoryBanksResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/memory_banks/create",
            body=maybe_transform(body, memory_bank_create_params.MemoryBankCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve(
        self,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/memory_banks/get",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"bank_id": bank_id}, memory_bank_retrieve_params.MemoryBankRetrieveParams),
            ),
            cast_to=object,
        )

    def update(
        self,
        *,
        bank_id: str,
        documents: Iterable[memory_bank_update_params.Document],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/memory_bank/update",
            body=maybe_transform(
                {
                    "bank_id": bank_id,
                    "documents": documents,
                },
                memory_bank_update_params.MemoryBankUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        extra_headers = {"Accept": "application/jsonl", **(extra_headers or {})}
        return self._get(
            "/memory_banks/list",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def drop(
        self,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/memory_banks/drop",
            body=maybe_transform({"bank_id": bank_id}, memory_bank_drop_params.MemoryBankDropParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    def insert(
        self,
        *,
        bank_id: str,
        documents: Iterable[memory_bank_insert_params.Document],
        ttl_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/memory_bank/insert",
            body=maybe_transform(
                {
                    "bank_id": bank_id,
                    "documents": documents,
                    "ttl_seconds": ttl_seconds,
                },
                memory_bank_insert_params.MemoryBankInsertParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def query(
        self,
        *,
        bank_id: str,
        query: Union[str, List[str]],
        params: Dict[str, Union[bool, float, str, Iterable[object], object, None]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QueryDocuments:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/memory_bank/query",
            body=maybe_transform(
                {
                    "bank_id": bank_id,
                    "query": query,
                    "params": params,
                },
                memory_bank_query_params.MemoryBankQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QueryDocuments,
        )


class AsyncMemoryBanksResource(AsyncAPIResource):
    @cached_property
    def documents(self) -> AsyncDocumentsResource:
        return AsyncDocumentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMemoryBanksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMemoryBanksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemoryBanksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AsyncMemoryBanksResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/memory_banks/create",
            body=await async_maybe_transform(body, memory_bank_create_params.MemoryBankCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve(
        self,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/memory_banks/get",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"bank_id": bank_id}, memory_bank_retrieve_params.MemoryBankRetrieveParams
                ),
            ),
            cast_to=object,
        )

    async def update(
        self,
        *,
        bank_id: str,
        documents: Iterable[memory_bank_update_params.Document],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/memory_bank/update",
            body=await async_maybe_transform(
                {
                    "bank_id": bank_id,
                    "documents": documents,
                },
                memory_bank_update_params.MemoryBankUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        extra_headers = {"Accept": "application/jsonl", **(extra_headers or {})}
        return await self._get(
            "/memory_banks/list",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def drop(
        self,
        *,
        bank_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/memory_banks/drop",
            body=await async_maybe_transform({"bank_id": bank_id}, memory_bank_drop_params.MemoryBankDropParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    async def insert(
        self,
        *,
        bank_id: str,
        documents: Iterable[memory_bank_insert_params.Document],
        ttl_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/memory_bank/insert",
            body=await async_maybe_transform(
                {
                    "bank_id": bank_id,
                    "documents": documents,
                    "ttl_seconds": ttl_seconds,
                },
                memory_bank_insert_params.MemoryBankInsertParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def query(
        self,
        *,
        bank_id: str,
        query: Union[str, List[str]],
        params: Dict[str, Union[bool, float, str, Iterable[object], object, None]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QueryDocuments:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/memory_bank/query",
            body=await async_maybe_transform(
                {
                    "bank_id": bank_id,
                    "query": query,
                    "params": params,
                },
                memory_bank_query_params.MemoryBankQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QueryDocuments,
        )


class MemoryBanksResourceWithRawResponse:
    def __init__(self, memory_banks: MemoryBanksResource) -> None:
        self._memory_banks = memory_banks

        self.create = to_raw_response_wrapper(
            memory_banks.create,
        )
        self.retrieve = to_raw_response_wrapper(
            memory_banks.retrieve,
        )
        self.update = to_raw_response_wrapper(
            memory_banks.update,
        )
        self.list = to_raw_response_wrapper(
            memory_banks.list,
        )
        self.drop = to_raw_response_wrapper(
            memory_banks.drop,
        )
        self.insert = to_raw_response_wrapper(
            memory_banks.insert,
        )
        self.query = to_raw_response_wrapper(
            memory_banks.query,
        )

    @cached_property
    def documents(self) -> DocumentsResourceWithRawResponse:
        return DocumentsResourceWithRawResponse(self._memory_banks.documents)


class AsyncMemoryBanksResourceWithRawResponse:
    def __init__(self, memory_banks: AsyncMemoryBanksResource) -> None:
        self._memory_banks = memory_banks

        self.create = async_to_raw_response_wrapper(
            memory_banks.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            memory_banks.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            memory_banks.update,
        )
        self.list = async_to_raw_response_wrapper(
            memory_banks.list,
        )
        self.drop = async_to_raw_response_wrapper(
            memory_banks.drop,
        )
        self.insert = async_to_raw_response_wrapper(
            memory_banks.insert,
        )
        self.query = async_to_raw_response_wrapper(
            memory_banks.query,
        )

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithRawResponse:
        return AsyncDocumentsResourceWithRawResponse(self._memory_banks.documents)


class MemoryBanksResourceWithStreamingResponse:
    def __init__(self, memory_banks: MemoryBanksResource) -> None:
        self._memory_banks = memory_banks

        self.create = to_streamed_response_wrapper(
            memory_banks.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            memory_banks.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            memory_banks.update,
        )
        self.list = to_streamed_response_wrapper(
            memory_banks.list,
        )
        self.drop = to_streamed_response_wrapper(
            memory_banks.drop,
        )
        self.insert = to_streamed_response_wrapper(
            memory_banks.insert,
        )
        self.query = to_streamed_response_wrapper(
            memory_banks.query,
        )

    @cached_property
    def documents(self) -> DocumentsResourceWithStreamingResponse:
        return DocumentsResourceWithStreamingResponse(self._memory_banks.documents)


class AsyncMemoryBanksResourceWithStreamingResponse:
    def __init__(self, memory_banks: AsyncMemoryBanksResource) -> None:
        self._memory_banks = memory_banks

        self.create = async_to_streamed_response_wrapper(
            memory_banks.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            memory_banks.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            memory_banks.update,
        )
        self.list = async_to_streamed_response_wrapper(
            memory_banks.list,
        )
        self.drop = async_to_streamed_response_wrapper(
            memory_banks.drop,
        )
        self.insert = async_to_streamed_response_wrapper(
            memory_banks.insert,
        )
        self.query = async_to_streamed_response_wrapper(
            memory_banks.query,
        )

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithStreamingResponse:
        return AsyncDocumentsResourceWithStreamingResponse(self._memory_banks.documents)

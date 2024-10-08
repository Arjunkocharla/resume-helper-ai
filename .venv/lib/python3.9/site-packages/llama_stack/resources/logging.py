# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import logging_get_logs_params, logging_log_messages_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.logging_get_logs_response import LoggingGetLogsResponse

__all__ = ["LoggingResource", "AsyncLoggingResource"]


class LoggingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LoggingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return LoggingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LoggingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return LoggingResourceWithStreamingResponse(self)

    def get_logs(
        self,
        *,
        request: logging_get_logs_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LoggingGetLogsResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/jsonl", **(extra_headers or {})}
        return self._post(
            "/logging/get_logs",
            body=maybe_transform({"request": request}, logging_get_logs_params.LoggingGetLogsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LoggingGetLogsResponse,
        )

    def log_messages(
        self,
        *,
        request: logging_log_messages_params.Request,
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
            "/logging/log_messages",
            body=maybe_transform({"request": request}, logging_log_messages_params.LoggingLogMessagesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncLoggingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLoggingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLoggingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLoggingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AsyncLoggingResourceWithStreamingResponse(self)

    async def get_logs(
        self,
        *,
        request: logging_get_logs_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LoggingGetLogsResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/jsonl", **(extra_headers or {})}
        return await self._post(
            "/logging/get_logs",
            body=await async_maybe_transform({"request": request}, logging_get_logs_params.LoggingGetLogsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LoggingGetLogsResponse,
        )

    async def log_messages(
        self,
        *,
        request: logging_log_messages_params.Request,
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
            "/logging/log_messages",
            body=await async_maybe_transform(
                {"request": request}, logging_log_messages_params.LoggingLogMessagesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class LoggingResourceWithRawResponse:
    def __init__(self, logging: LoggingResource) -> None:
        self._logging = logging

        self.get_logs = to_raw_response_wrapper(
            logging.get_logs,
        )
        self.log_messages = to_raw_response_wrapper(
            logging.log_messages,
        )


class AsyncLoggingResourceWithRawResponse:
    def __init__(self, logging: AsyncLoggingResource) -> None:
        self._logging = logging

        self.get_logs = async_to_raw_response_wrapper(
            logging.get_logs,
        )
        self.log_messages = async_to_raw_response_wrapper(
            logging.log_messages,
        )


class LoggingResourceWithStreamingResponse:
    def __init__(self, logging: LoggingResource) -> None:
        self._logging = logging

        self.get_logs = to_streamed_response_wrapper(
            logging.get_logs,
        )
        self.log_messages = to_streamed_response_wrapper(
            logging.log_messages,
        )


class AsyncLoggingResourceWithStreamingResponse:
    def __init__(self, logging: AsyncLoggingResource) -> None:
        self._logging = logging

        self.get_logs = async_to_streamed_response_wrapper(
            logging.get_logs,
        )
        self.log_messages = async_to_streamed_response_wrapper(
            logging.log_messages,
        )

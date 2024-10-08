# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .steps import (
    StepsResource,
    AsyncStepsResource,
    StepsResourceWithRawResponse,
    AsyncStepsResourceWithRawResponse,
    StepsResourceWithStreamingResponse,
    AsyncStepsResourceWithStreamingResponse,
)
from .turns import (
    TurnsResource,
    AsyncTurnsResource,
    TurnsResourceWithRawResponse,
    AsyncTurnsResourceWithRawResponse,
    TurnsResourceWithStreamingResponse,
    AsyncTurnsResourceWithStreamingResponse,
)
from ...types import agentic_system_create_params, agentic_system_delete_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .sessions import (
    SessionsResource,
    AsyncSessionsResource,
    SessionsResourceWithRawResponse,
    AsyncSessionsResourceWithRawResponse,
    SessionsResourceWithStreamingResponse,
    AsyncSessionsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.agentic_system_create_response import AgenticSystemCreateResponse

__all__ = ["AgenticSystemResource", "AsyncAgenticSystemResource"]


class AgenticSystemResource(SyncAPIResource):
    @cached_property
    def sessions(self) -> SessionsResource:
        return SessionsResource(self._client)

    @cached_property
    def steps(self) -> StepsResource:
        return StepsResource(self._client)

    @cached_property
    def turns(self) -> TurnsResource:
        return TurnsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AgenticSystemResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AgenticSystemResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgenticSystemResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AgenticSystemResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        agent_config: agentic_system_create_params.AgentConfig,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgenticSystemCreateResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agentic_system/create",
            body=maybe_transform(
                {"agent_config": agent_config}, agentic_system_create_params.AgenticSystemCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgenticSystemCreateResponse,
        )

    def delete(
        self,
        *,
        agent_id: str,
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
            "/agentic_system/delete",
            body=maybe_transform({"agent_id": agent_id}, agentic_system_delete_params.AgenticSystemDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncAgenticSystemResource(AsyncAPIResource):
    @cached_property
    def sessions(self) -> AsyncSessionsResource:
        return AsyncSessionsResource(self._client)

    @cached_property
    def steps(self) -> AsyncStepsResource:
        return AsyncStepsResource(self._client)

    @cached_property
    def turns(self) -> AsyncTurnsResource:
        return AsyncTurnsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAgenticSystemResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAgenticSystemResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgenticSystemResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AsyncAgenticSystemResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        agent_config: agentic_system_create_params.AgentConfig,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgenticSystemCreateResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agentic_system/create",
            body=await async_maybe_transform(
                {"agent_config": agent_config}, agentic_system_create_params.AgenticSystemCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgenticSystemCreateResponse,
        )

    async def delete(
        self,
        *,
        agent_id: str,
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
            "/agentic_system/delete",
            body=await async_maybe_transform(
                {"agent_id": agent_id}, agentic_system_delete_params.AgenticSystemDeleteParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AgenticSystemResourceWithRawResponse:
    def __init__(self, agentic_system: AgenticSystemResource) -> None:
        self._agentic_system = agentic_system

        self.create = to_raw_response_wrapper(
            agentic_system.create,
        )
        self.delete = to_raw_response_wrapper(
            agentic_system.delete,
        )

    @cached_property
    def sessions(self) -> SessionsResourceWithRawResponse:
        return SessionsResourceWithRawResponse(self._agentic_system.sessions)

    @cached_property
    def steps(self) -> StepsResourceWithRawResponse:
        return StepsResourceWithRawResponse(self._agentic_system.steps)

    @cached_property
    def turns(self) -> TurnsResourceWithRawResponse:
        return TurnsResourceWithRawResponse(self._agentic_system.turns)


class AsyncAgenticSystemResourceWithRawResponse:
    def __init__(self, agentic_system: AsyncAgenticSystemResource) -> None:
        self._agentic_system = agentic_system

        self.create = async_to_raw_response_wrapper(
            agentic_system.create,
        )
        self.delete = async_to_raw_response_wrapper(
            agentic_system.delete,
        )

    @cached_property
    def sessions(self) -> AsyncSessionsResourceWithRawResponse:
        return AsyncSessionsResourceWithRawResponse(self._agentic_system.sessions)

    @cached_property
    def steps(self) -> AsyncStepsResourceWithRawResponse:
        return AsyncStepsResourceWithRawResponse(self._agentic_system.steps)

    @cached_property
    def turns(self) -> AsyncTurnsResourceWithRawResponse:
        return AsyncTurnsResourceWithRawResponse(self._agentic_system.turns)


class AgenticSystemResourceWithStreamingResponse:
    def __init__(self, agentic_system: AgenticSystemResource) -> None:
        self._agentic_system = agentic_system

        self.create = to_streamed_response_wrapper(
            agentic_system.create,
        )
        self.delete = to_streamed_response_wrapper(
            agentic_system.delete,
        )

    @cached_property
    def sessions(self) -> SessionsResourceWithStreamingResponse:
        return SessionsResourceWithStreamingResponse(self._agentic_system.sessions)

    @cached_property
    def steps(self) -> StepsResourceWithStreamingResponse:
        return StepsResourceWithStreamingResponse(self._agentic_system.steps)

    @cached_property
    def turns(self) -> TurnsResourceWithStreamingResponse:
        return TurnsResourceWithStreamingResponse(self._agentic_system.turns)


class AsyncAgenticSystemResourceWithStreamingResponse:
    def __init__(self, agentic_system: AsyncAgenticSystemResource) -> None:
        self._agentic_system = agentic_system

        self.create = async_to_streamed_response_wrapper(
            agentic_system.create,
        )
        self.delete = async_to_streamed_response_wrapper(
            agentic_system.delete,
        )

    @cached_property
    def sessions(self) -> AsyncSessionsResourceWithStreamingResponse:
        return AsyncSessionsResourceWithStreamingResponse(self._agentic_system.sessions)

    @cached_property
    def steps(self) -> AsyncStepsResourceWithStreamingResponse:
        return AsyncStepsResourceWithStreamingResponse(self._agentic_system.steps)

    @cached_property
    def turns(self) -> AsyncTurnsResourceWithStreamingResponse:
        return AsyncTurnsResourceWithStreamingResponse(self._agentic_system.turns)

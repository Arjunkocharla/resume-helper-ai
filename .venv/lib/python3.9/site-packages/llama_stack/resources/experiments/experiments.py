# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import (
    experiment_create_params,
    experiment_update_params,
    experiment_retrieve_params,
    experiment_create_run_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .artifacts import (
    ArtifactsResource,
    AsyncArtifactsResource,
    ArtifactsResourceWithRawResponse,
    AsyncArtifactsResourceWithRawResponse,
    ArtifactsResourceWithStreamingResponse,
    AsyncArtifactsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.experiment import Experiment
from ...types.shared.run import Run

__all__ = ["ExperimentsResource", "AsyncExperimentsResource"]


class ExperimentsResource(SyncAPIResource):
    @cached_property
    def artifacts(self) -> ArtifactsResource:
        return ArtifactsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ExperimentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return ExperimentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExperimentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return ExperimentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        request: experiment_create_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Experiment:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/experiments/create",
            body=maybe_transform({"request": request}, experiment_create_params.ExperimentCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Experiment,
        )

    def retrieve(
        self,
        *,
        experiment_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Experiment:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/experiments/get",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"experiment_id": experiment_id}, experiment_retrieve_params.ExperimentRetrieveParams
                ),
            ),
            cast_to=Experiment,
        )

    def update(
        self,
        *,
        request: experiment_update_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Experiment:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/experiments/update",
            body=maybe_transform({"request": request}, experiment_update_params.ExperimentUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Experiment,
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
    ) -> Experiment:
        extra_headers = {"Accept": "application/jsonl", **(extra_headers or {})}
        return self._get(
            "/experiments/list",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Experiment,
        )

    def create_run(
        self,
        *,
        request: experiment_create_run_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Run:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/experiments/create_run",
            body=maybe_transform({"request": request}, experiment_create_run_params.ExperimentCreateRunParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Run,
        )


class AsyncExperimentsResource(AsyncAPIResource):
    @cached_property
    def artifacts(self) -> AsyncArtifactsResource:
        return AsyncArtifactsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncExperimentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncExperimentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExperimentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AsyncExperimentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        request: experiment_create_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Experiment:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/experiments/create",
            body=await async_maybe_transform({"request": request}, experiment_create_params.ExperimentCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Experiment,
        )

    async def retrieve(
        self,
        *,
        experiment_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Experiment:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/experiments/get",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"experiment_id": experiment_id}, experiment_retrieve_params.ExperimentRetrieveParams
                ),
            ),
            cast_to=Experiment,
        )

    async def update(
        self,
        *,
        request: experiment_update_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Experiment:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/experiments/update",
            body=await async_maybe_transform({"request": request}, experiment_update_params.ExperimentUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Experiment,
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
    ) -> Experiment:
        extra_headers = {"Accept": "application/jsonl", **(extra_headers or {})}
        return await self._get(
            "/experiments/list",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Experiment,
        )

    async def create_run(
        self,
        *,
        request: experiment_create_run_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Run:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/experiments/create_run",
            body=await async_maybe_transform(
                {"request": request}, experiment_create_run_params.ExperimentCreateRunParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Run,
        )


class ExperimentsResourceWithRawResponse:
    def __init__(self, experiments: ExperimentsResource) -> None:
        self._experiments = experiments

        self.create = to_raw_response_wrapper(
            experiments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            experiments.retrieve,
        )
        self.update = to_raw_response_wrapper(
            experiments.update,
        )
        self.list = to_raw_response_wrapper(
            experiments.list,
        )
        self.create_run = to_raw_response_wrapper(
            experiments.create_run,
        )

    @cached_property
    def artifacts(self) -> ArtifactsResourceWithRawResponse:
        return ArtifactsResourceWithRawResponse(self._experiments.artifacts)


class AsyncExperimentsResourceWithRawResponse:
    def __init__(self, experiments: AsyncExperimentsResource) -> None:
        self._experiments = experiments

        self.create = async_to_raw_response_wrapper(
            experiments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            experiments.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            experiments.update,
        )
        self.list = async_to_raw_response_wrapper(
            experiments.list,
        )
        self.create_run = async_to_raw_response_wrapper(
            experiments.create_run,
        )

    @cached_property
    def artifacts(self) -> AsyncArtifactsResourceWithRawResponse:
        return AsyncArtifactsResourceWithRawResponse(self._experiments.artifacts)


class ExperimentsResourceWithStreamingResponse:
    def __init__(self, experiments: ExperimentsResource) -> None:
        self._experiments = experiments

        self.create = to_streamed_response_wrapper(
            experiments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            experiments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            experiments.update,
        )
        self.list = to_streamed_response_wrapper(
            experiments.list,
        )
        self.create_run = to_streamed_response_wrapper(
            experiments.create_run,
        )

    @cached_property
    def artifacts(self) -> ArtifactsResourceWithStreamingResponse:
        return ArtifactsResourceWithStreamingResponse(self._experiments.artifacts)


class AsyncExperimentsResourceWithStreamingResponse:
    def __init__(self, experiments: AsyncExperimentsResource) -> None:
        self._experiments = experiments

        self.create = async_to_streamed_response_wrapper(
            experiments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            experiments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            experiments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            experiments.list,
        )
        self.create_run = async_to_streamed_response_wrapper(
            experiments.create_run,
        )

    @cached_property
    def artifacts(self) -> AsyncArtifactsResourceWithStreamingResponse:
        return AsyncArtifactsResourceWithStreamingResponse(self._experiments.artifacts)

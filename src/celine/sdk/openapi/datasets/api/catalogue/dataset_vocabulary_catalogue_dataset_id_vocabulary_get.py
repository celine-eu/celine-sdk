from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    dataset_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/catalogue/{dataset_id}/vocabulary".format(
            dataset_id=quote(str(dataset_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Dataset Vocabulary

     The JSON-LD context for this dataset, derived from its mapping spec.

    Unauthenticated, like `/catalogue`. A consumer decides whether it *can* read
    a dataset before it negotiates access, so gating the vocabulary would gate
    discovery — and the vocabulary describes the shape of the data, not the data.

    404 means the dataset is not exposed **or** declares no mapping. That is not
    the same as \"this dataset has no semantic model\", and a consumer should not
    read it as such; the catalogue entry's `dct:conformsTo` is where a declared
    model is stated.

    Args:
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Dataset Vocabulary

     The JSON-LD context for this dataset, derived from its mapping spec.

    Unauthenticated, like `/catalogue`. A consumer decides whether it *can* read
    a dataset before it negotiates access, so gating the vocabulary would gate
    discovery — and the vocabulary describes the shape of the data, not the data.

    404 means the dataset is not exposed **or** declares no mapping. That is not
    the same as \"this dataset has no semantic model\", and a consumer should not
    read it as such; the catalogue entry's `dct:conformsTo` is where a declared
    model is stated.

    Args:
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    r"""Dataset Vocabulary

     The JSON-LD context for this dataset, derived from its mapping spec.

    Unauthenticated, like `/catalogue`. A consumer decides whether it *can* read
    a dataset before it negotiates access, so gating the vocabulary would gate
    discovery — and the vocabulary describes the shape of the data, not the data.

    404 means the dataset is not exposed **or** declares no mapping. That is not
    the same as \"this dataset has no semantic model\", and a consumer should not
    read it as such; the catalogue entry's `dct:conformsTo` is where a declared
    model is stated.

    Args:
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    r"""Dataset Vocabulary

     The JSON-LD context for this dataset, derived from its mapping spec.

    Unauthenticated, like `/catalogue`. A consumer decides whether it *can* read
    a dataset before it negotiates access, so gating the vocabulary would gate
    discovery — and the vocabulary describes the shape of the data, not the data.

    404 means the dataset is not exposed **or** declares no mapping. That is not
    the same as \"this dataset has no semantic model\", and a consumer should not
    read it as such; the catalogue entry's `dct:conformsTo` is where a declared
    model is stated.

    Args:
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
        )
    ).parsed

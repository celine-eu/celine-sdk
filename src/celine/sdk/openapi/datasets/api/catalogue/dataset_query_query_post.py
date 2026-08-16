from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_query_model import DatasetQueryModel
from ...models.dataset_query_result import DatasetQueryResult
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DatasetQueryModel,
    authorization: None | str | Unset = UNSET,
    edc_contract_agreement_id: None | str | Unset = UNSET,
    edc_transfer_process_id: None | str | Unset = UNSET,
    edc_purpose: None | str | Unset = UNSET,
    edc_bpn: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    if not isinstance(edc_contract_agreement_id, Unset):
        headers["edc-contract-agreement-id"] = edc_contract_agreement_id

    if not isinstance(edc_transfer_process_id, Unset):
        headers["edc-transfer-process-id"] = edc_transfer_process_id

    if not isinstance(edc_purpose, Unset):
        headers["edc-purpose"] = edc_purpose

    if not isinstance(edc_bpn, Unset):
        headers["edc-bpn"] = edc_bpn

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/query",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DatasetQueryResult | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DatasetQueryResult.from_dict(response.json())

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
) -> Response[DatasetQueryResult | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DatasetQueryModel,
    authorization: None | str | Unset = UNSET,
    edc_contract_agreement_id: None | str | Unset = UNSET,
    edc_transfer_process_id: None | str | Unset = UNSET,
    edc_purpose: None | str | Unset = UNSET,
    edc_bpn: None | str | Unset = UNSET,
) -> Response[DatasetQueryResult | HTTPValidationError]:
    """Dataset Query

     Query available datasets

    Args:
        authorization (None | str | Unset):
        edc_contract_agreement_id (None | str | Unset):
        edc_transfer_process_id (None | str | Unset):
        edc_purpose (None | str | Unset):
        edc_bpn (None | str | Unset):
        body (DatasetQueryModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetQueryResult | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
        edc_contract_agreement_id=edc_contract_agreement_id,
        edc_transfer_process_id=edc_transfer_process_id,
        edc_purpose=edc_purpose,
        edc_bpn=edc_bpn,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: DatasetQueryModel,
    authorization: None | str | Unset = UNSET,
    edc_contract_agreement_id: None | str | Unset = UNSET,
    edc_transfer_process_id: None | str | Unset = UNSET,
    edc_purpose: None | str | Unset = UNSET,
    edc_bpn: None | str | Unset = UNSET,
) -> DatasetQueryResult | HTTPValidationError | None:
    """Dataset Query

     Query available datasets

    Args:
        authorization (None | str | Unset):
        edc_contract_agreement_id (None | str | Unset):
        edc_transfer_process_id (None | str | Unset):
        edc_purpose (None | str | Unset):
        edc_bpn (None | str | Unset):
        body (DatasetQueryModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetQueryResult | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
        edc_contract_agreement_id=edc_contract_agreement_id,
        edc_transfer_process_id=edc_transfer_process_id,
        edc_purpose=edc_purpose,
        edc_bpn=edc_bpn,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DatasetQueryModel,
    authorization: None | str | Unset = UNSET,
    edc_contract_agreement_id: None | str | Unset = UNSET,
    edc_transfer_process_id: None | str | Unset = UNSET,
    edc_purpose: None | str | Unset = UNSET,
    edc_bpn: None | str | Unset = UNSET,
) -> Response[DatasetQueryResult | HTTPValidationError]:
    """Dataset Query

     Query available datasets

    Args:
        authorization (None | str | Unset):
        edc_contract_agreement_id (None | str | Unset):
        edc_transfer_process_id (None | str | Unset):
        edc_purpose (None | str | Unset):
        edc_bpn (None | str | Unset):
        body (DatasetQueryModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetQueryResult | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
        edc_contract_agreement_id=edc_contract_agreement_id,
        edc_transfer_process_id=edc_transfer_process_id,
        edc_purpose=edc_purpose,
        edc_bpn=edc_bpn,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: DatasetQueryModel,
    authorization: None | str | Unset = UNSET,
    edc_contract_agreement_id: None | str | Unset = UNSET,
    edc_transfer_process_id: None | str | Unset = UNSET,
    edc_purpose: None | str | Unset = UNSET,
    edc_bpn: None | str | Unset = UNSET,
) -> DatasetQueryResult | HTTPValidationError | None:
    """Dataset Query

     Query available datasets

    Args:
        authorization (None | str | Unset):
        edc_contract_agreement_id (None | str | Unset):
        edc_transfer_process_id (None | str | Unset):
        edc_purpose (None | str | Unset):
        edc_bpn (None | str | Unset):
        body (DatasetQueryModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetQueryResult | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
            edc_contract_agreement_id=edc_contract_agreement_id,
            edc_transfer_process_id=edc_transfer_process_id,
            edc_purpose=edc_purpose,
            edc_bpn=edc_bpn,
        )
    ).parsed

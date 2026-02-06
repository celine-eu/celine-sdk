from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.mqtt_acl_request import MqttAclRequest
from ...models.mqtt_response import MqttResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: MqttAclRequest,
    authorization: None | str | Unset = UNSET,
    x_request_id: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    if not isinstance(x_request_id, Unset):
        headers["x-request-id"] = x_request_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/mqtt/acl",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | MqttResponse | None:
    if response.status_code == 200:
        response_200 = MqttResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | MqttResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MqttAclRequest,
    authorization: None | str | Unset = UNSET,
    x_request_id: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | MqttResponse]:
    """Mqtt Acl

     Authorize MQTT topic access.

    Args:
        authorization (None | str | Unset):
        x_request_id (None | str | Unset):
        body (MqttAclRequest): MQTT ACL check request (mosquitto-go-auth format).

            mosquitto ACL checks use a bitmask:
            - MOSQ_ACL_READ      0x01
            - MOSQ_ACL_WRITE     0x02
            - MOSQ_ACL_SUBSCRIBE 0x04

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MqttResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
        x_request_id=x_request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: MqttAclRequest,
    authorization: None | str | Unset = UNSET,
    x_request_id: None | str | Unset = UNSET,
) -> HTTPValidationError | MqttResponse | None:
    """Mqtt Acl

     Authorize MQTT topic access.

    Args:
        authorization (None | str | Unset):
        x_request_id (None | str | Unset):
        body (MqttAclRequest): MQTT ACL check request (mosquitto-go-auth format).

            mosquitto ACL checks use a bitmask:
            - MOSQ_ACL_READ      0x01
            - MOSQ_ACL_WRITE     0x02
            - MOSQ_ACL_SUBSCRIBE 0x04

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MqttResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MqttAclRequest,
    authorization: None | str | Unset = UNSET,
    x_request_id: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | MqttResponse]:
    """Mqtt Acl

     Authorize MQTT topic access.

    Args:
        authorization (None | str | Unset):
        x_request_id (None | str | Unset):
        body (MqttAclRequest): MQTT ACL check request (mosquitto-go-auth format).

            mosquitto ACL checks use a bitmask:
            - MOSQ_ACL_READ      0x01
            - MOSQ_ACL_WRITE     0x02
            - MOSQ_ACL_SUBSCRIBE 0x04

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MqttResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: MqttAclRequest,
    authorization: None | str | Unset = UNSET,
    x_request_id: None | str | Unset = UNSET,
) -> HTTPValidationError | MqttResponse | None:
    """Mqtt Acl

     Authorize MQTT topic access.

    Args:
        authorization (None | str | Unset):
        x_request_id (None | str | Unset):
        body (MqttAclRequest): MQTT ACL check request (mosquitto-go-auth format).

            mosquitto ACL checks use a bitmask:
            - MOSQ_ACL_READ      0x01
            - MOSQ_ACL_WRITE     0x02
            - MOSQ_ACL_SUBSCRIBE 0x04

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MqttResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
            x_request_id=x_request_id,
        )
    ).parsed

from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_get_scenario_simulations_simulation_key_scenarios_scenario_id_get import (
    ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet,
)
from ...types import Response


def _get_kwargs(
    simulation_key: str,
    scenario_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/simulations/{simulation_key}/scenarios/{scenario_id}".format(
            simulation_key=quote(str(simulation_key), safe=""),
            scenario_id=quote(str(scenario_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet | None:
    if response.status_code == 200:
        response_200 = ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    simulation_key: str,
    scenario_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet]:
    """Get Scenario

    Args:
        simulation_key (str):
        scenario_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
        scenario_id=scenario_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    simulation_key: str,
    scenario_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet | None:
    """Get Scenario

    Args:
        simulation_key (str):
        scenario_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet
    """

    return sync_detailed(
        simulation_key=simulation_key,
        scenario_id=scenario_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    simulation_key: str,
    scenario_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet]:
    """Get Scenario

    Args:
        simulation_key (str):
        scenario_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
        scenario_id=scenario_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    simulation_key: str,
    scenario_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet | None:
    """Get Scenario

    Args:
        simulation_key (str):
        scenario_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseGetScenarioSimulationsSimulationKeyScenariosScenarioIdGet
    """

    return (
        await asyncio_detailed(
            simulation_key=simulation_key,
            scenario_id=scenario_id,
            client=client,
        )
    ).parsed

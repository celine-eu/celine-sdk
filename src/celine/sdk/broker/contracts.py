from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Awaitable, Callable, Protocol


class QoS(Enum):
    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2


@dataclass(frozen=True)
class BrokerMessage:
    topic: str
    payload: dict[str, Any]
    qos: QoS = QoS.AT_LEAST_ONCE
    retain: bool = False


@dataclass(frozen=True)
class PublishResult:
    success: bool
    message_id: str | None = None
    error: str | None = None


@dataclass(frozen=True)
class SubscribeResult:
    subscription_id: str


@dataclass(frozen=True)
class ReceivedMessage:
    topic: str
    payload: dict[str, Any]
    raw_payload: bytes
    qos: QoS
    message_id: str | None
    timestamp: datetime


MessageHandler = Callable[[ReceivedMessage], Awaitable[None]]


class Broker(Protocol):
    async def __aenter__(self) -> "Broker": ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    async def publish(self, message: BrokerMessage) -> PublishResult: ...
    async def subscribe(self, topics: list[str], handler: MessageHandler, qos: QoS = QoS.AT_LEAST_ONCE) -> SubscribeResult: ...
    async def unsubscribe(self, subscription_id: str) -> bool: ...


class BrokerBase(ABC):
    @abstractmethod
    async def publish(self, message: BrokerMessage) -> PublishResult:
        raise NotImplementedError

    @abstractmethod
    async def subscribe(self, topics: list[str], handler: MessageHandler, qos: QoS = QoS.AT_LEAST_ONCE) -> SubscribeResult:
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, subscription_id: str) -> bool:
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

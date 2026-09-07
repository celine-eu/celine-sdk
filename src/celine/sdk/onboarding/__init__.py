"""Onboarding API wrapper."""

from celine.sdk.onboarding.client import OnboardingClient
from celine.sdk.onboarding.errors import OnboardingApiError

__all__ = ["OnboardingClient", "OnboardingApiError"]

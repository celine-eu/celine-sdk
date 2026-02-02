from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

from celine.sdk.settings.models import SdkSettings

_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(:-([^}]*))?\}")


def _resolve_env_str(s: str) -> str:
    def repl(m: re.Match[str]) -> str:
        var = m.group(1)
        default = m.group(3)
        val = os.getenv(var)
        if val is None or val == "":
            return default or ""
        return val

    # Resolve repeatedly until stable (handles nested defaults)
    prev = None
    cur = s
    for _ in range(5):
        if cur == prev:
            break
        prev = cur
        cur = _ENV_PATTERN.sub(repl, cur)
    return cur


def _resolve_env(value: Any) -> Any:
    if isinstance(value, str):
        return _resolve_env_str(value)
    if isinstance(value, list):
        return [_resolve_env(v) for v in value]
    if isinstance(value, dict):
        return {k: _resolve_env(v) for k, v in value.items()}
    return value


def load_settings(path: str | Path | None = None) -> SdkSettings:
    """Load settings from env + optional YAML overlay.

    YAML values support ${VAR} and ${VAR:-default}.

    If path is None, only environment variables are used.
    """
    base = SdkSettings()
    if path is None:
        return base

    p = Path(path)
    data: dict[str, Any] = {}
    if p.exists():
        raw = yaml.safe_load(p.read_text()) or {}
        if not isinstance(raw, dict):
            raise ValueError(f"Settings YAML must be a mapping, got {type(raw)}")
        data = _resolve_env(raw)

    # Let YAML override env-derived base
    merged = base.model_dump()
    merged.update(data)
    return SdkSettings.model_validate(merged)

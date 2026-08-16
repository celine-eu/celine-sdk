from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import httpx
import yaml


def parse_openapi_bytes(content: bytes) -> dict[str, Any]:
    # Try JSON first
    try:
        return json.loads(content)
    except Exception:
        pass
    # YAML fallback
    obj = yaml.safe_load(content.decode("utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("OpenAPI spec must be an object")
    return obj


def spec_version(spec: dict[str, Any]) -> str:
    info = spec.get("info") or {}
    v = info.get("version")
    if not isinstance(v, str) or not v:
        raise ValueError("OpenAPI spec missing info.version")
    return v


def fetch_spec(url: str, timeout: float = 20.0) -> dict[str, Any]:
    r = httpx.get(url, timeout=timeout)
    r.raise_for_status()
    return parse_openapi_bytes(r.content)


def write_spec(root: Path, service: str, version: str, spec: dict[str, Any]) -> Path:
    base = root / service
    ver_dir = base / f"v{version}"
    ver_dir.mkdir(parents=True, exist_ok=True)
    path = ver_dir / "openapi.json"
    path.write_text(json.dumps(spec, indent=2, sort_keys=True))

    return path


_VERSION_PART = re.compile(r"^(\d+)(.*)$")


def version_key(name: str) -> tuple[tuple[int, int, str], ...]:
    """Order `v<version>` directory names by number, not by character.

    Plain sorting put `v0.10.0` before `v0.2.0`, which made `latest_version`
    return an older spec the moment a service reached a double-digit component —
    and generation would then quietly build clients from it.

    Each dotted component sorts numerically where it starts with digits, and
    after every numeric one where it does not. Full semantic-version precedence
    is not implemented: a pre-release suffix sorts *after* the release it
    qualifies, which is the opposite of semver but keeps this a total order over
    whatever a service happens to put in `info.version`.
    """
    raw = name[1:] if name.startswith("v") else name
    key: list[tuple[int, int, str]] = []
    for part in re.split(r"[.\-+_]", raw):
        match = _VERSION_PART.match(part)
        if match:
            key.append((0, int(match.group(1)), match.group(2)))
        else:
            key.append((1, 0, part))
    return tuple(key)


def list_versions(root: Path, service: str) -> list[str]:
    base = root / service
    if not base.exists():
        return []
    versions = []
    for p in base.iterdir():
        if p.is_dir() and p.name.startswith("v"):
            versions.append(p.name)
    return sorted(versions, key=version_key)


def latest_version(root: Path, service: str) -> str | None:
    vs = list_versions(root, service)
    if not vs:
        return None
    return vs[-1]

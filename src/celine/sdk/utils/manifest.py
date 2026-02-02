from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ServiceEntry(BaseModel):
    openapi: str = Field(..., description="OpenAPI URL")
    package: str | None = Field(default=None, description="Override package slug")


class ServicesManifest(BaseModel):
    services: dict[str, ServiceEntry]


def load_manifest(path: str | Path) -> ServicesManifest:
    p = Path(path)
    raw = yaml.safe_load(p.read_text())
    if not isinstance(raw, dict):
        raise ValueError("services.yaml must be a mapping")
    return ServicesManifest.model_validate(raw)


def package_slug(service_name: str, override: str | None) -> str:
    slug = override or service_name
    # Normalize to python identifier-like
    out = []
    for ch in slug.lower():
        if ch.isalnum():
            out.append(ch)
        else:
            out.append("_")
    s = "".join(out)
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_") or "service"

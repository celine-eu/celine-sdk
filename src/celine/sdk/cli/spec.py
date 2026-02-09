from __future__ import annotations

from pathlib import Path
import shutil

import typer

from celine.sdk.utils.manifest import load_manifest
from celine.sdk.utils.openapi_specs import (
    fetch_spec,
    spec_version,
    write_spec,
    list_versions,
    latest_version,
)

spec_app = typer.Typer(add_completion=False, help="Manage versioned OpenAPI specs")


@spec_app.command("fetch")
def fetch(
    manifest_path: str = typer.Argument(
        default=Path("./services.yaml"), help="Path to services.yaml"
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        help="Clean destination folder",
    ),
    out_dir: str = typer.Option("openapi", help="Output directory"),
) -> None:
    mf = load_manifest(manifest_path)
    root = Path(out_dir)

    if root.exists() and clean:
        typer.echo(f"Removing output dir {root}")
        shutil.rmtree(out_dir)

    root.mkdir(parents=True, exist_ok=True)

    for name, entry in mf.services.items():
        try:
            spec = fetch_spec(entry.openapi)
            ver = spec_version(spec)
            path = write_spec(root, name, ver, spec)
            typer.echo(f"{name}: wrote {path}")
        except Exception as e:
            typer.echo(f"{name}: failed to load spec {e}")


@spec_app.command("list")
def list_cmd(
    out_dir: str = typer.Option("openapi", help="Specs directory"),
) -> None:
    root = Path(out_dir)
    if not root.exists():
        typer.echo("No specs directory")
        raise typer.Exit(code=1)

    for svc in sorted([p.name for p in root.iterdir() if p.is_dir()]):
        versions = list_versions(root, svc)
        latest = latest_version(root, svc)
        if not versions:
            continue
        typer.echo(f"{svc}: {', '.join(versions)} (latest={latest})")

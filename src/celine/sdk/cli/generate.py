from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import typer

from celine.sdk.utils.manifest import load_manifest, package_slug
from celine.sdk.utils.openapi_specs import latest_version

gen_app = typer.Typer(
    add_completion=False, help="Generate clients from versioned specs"
)


def _write_config(path: Path, package_name: str) -> None:
    path.write_text(
        "\n".join(
            [
                "package_name: %s" % package_name,
                "use_path_prefixes_for_title_model_names: false",
            ]
        )
        + "\n"
    )


def _generate_openapi_client(spec_path: Path, out_dir: Path, package_name: str) -> None:
    cfg = out_dir / "openapi-python-client.yml"
    _write_config(cfg, package_name)

    cmd = [
        "openapi-python-client",
        "generate",
        "--path",
        str(spec_path),
        "--output-path",
        str(out_dir),
        "--overwrite",
        "--config",
        str(cfg),
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.stdout:
        typer.echo(proc.stdout)
    if proc.stderr:
        typer.echo(proc.stderr, err=True)

    if proc.returncode != 0:
        raise RuntimeError(
            "openapi-python-client failed\nSTDOUT:\n%s\nSTDERR:\n%s"
            % (proc.stdout, proc.stderr)
        )


def _generate_openapi_schemas(spec_path: Path, schemas_path: Path) -> None:
    cmd = [
        "datamodel-codegen",
        "--input",
        str(spec_path),
        "--input-file-type",
        "openapi",
        "--output",
        str(schemas_path),
        "--class-name-suffix",
        "Schema",
        "--use-title-as-name",
        "--collapse-root-models",
        "--use-schema-description",
        "--formatters",
        "ruff-format",
        "--formatters",
        "ruff-check",
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.stdout:
        typer.echo(proc.stdout)
    if proc.stderr:
        typer.echo(proc.stderr, err=True)

    if proc.returncode != 0:
        raise RuntimeError(
            "datamodel-code-generator failed\nSTDOUT:\n%s\nSTDERR:\n%s"
            % (proc.stdout, proc.stderr)
        )

    typer.echo(f"Wrote schemas to: {schemas_path}")


@gen_app.callback(invoke_without_command=True)
def generate(
    manifest_path: str = typer.Argument(
        default=Path("services.yaml"), help="Path to services.yaml"
    ),
    specs_dir: str = typer.Option("openapi", help="Versioned specs directory"),
    dest_root: str = typer.Option(
        "src/celine/sdk/openapi", help="Destination package root"
    ),
) -> None:
    """Generate (or update) clients under celine.sdk.openapi.<package>."""
    mf = load_manifest(manifest_path)
    specs_root = Path(specs_dir)
    dest_root_path = Path(dest_root)
    dest_root_path.mkdir(parents=True, exist_ok=True)

    for svc_name, entry in mf.services.items():
        pkg = package_slug(svc_name, entry.package)
        ver = latest_version(specs_root, svc_name)
        if ver is None:
            raise RuntimeError(
                f"No specs found for {svc_name}. Run: celine-sdk spec fetch ..."
            )

        spec_path = specs_root / svc_name / ver / "openapi.json"
        if not spec_path.exists():
            raise RuntimeError(f"Spec missing: {spec_path}")

        typer.echo(
            f"Generating {svc_name} -> celine.sdk.openapi.{pkg} from {spec_path}"
        )

        with tempfile.TemporaryDirectory(prefix=f"celine-sdk-{pkg}-") as td:
            out_dir = Path(td)
            _generate_openapi_client(spec_path, out_dir, pkg)

            generated_pkg_dir = out_dir / pkg
            if not generated_pkg_dir.exists():
                # Some versions generate into a project folder; attempt to locate
                candidates = [
                    p
                    for p in out_dir.iterdir()
                    if p.is_dir() and (p / "__init__.py").exists()
                ]
                if len(candidates) == 1:
                    generated_pkg_dir = candidates[0]
                else:
                    raise RuntimeError(
                        f"Could not find generated package '{pkg}' in {out_dir}. Found: {candidates}"
                    )

            dest_dir = dest_root_path / pkg
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(generated_pkg_dir, dest_dir)

        _generate_openapi_schemas(spec_path, dest_dir / "schemas.py")

        typer.echo(f"Wrote: {dest_dir}")

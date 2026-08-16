"""Tests for the spec CLI and the generated-code boundary.

See docs/specifications/spec-management.md. Nothing here reaches the network or
runs a code generator: what is asserted is this repository's own logic —
versioning, manifest handling, orchestration and the conversion helpers that
every service uses to hold a Pydantic model on one side of a generated client.
"""

from __future__ import annotations

import json
from http import HTTPStatus
from pathlib import Path

import pytest
from pydantic import BaseModel, Field

from celine.sdk.cli import generate as generate_cli
from celine.sdk.cli import spec as spec_cli
from celine.sdk.dt.util import DTApiError, unwrap
from celine.sdk.openapi.dt.types import Response
from celine.sdk.utils.convert import to_client, to_schema
from celine.sdk.utils.manifest import load_manifest, package_slug
from celine.sdk.utils.openapi_specs import (
    latest_version,
    list_versions,
    parse_openapi_bytes,
    spec_version,
    write_spec,
)

MANIFEST = """
services:
  digital-twin:
    package: dt
    openapi: http://dt:8000/openapi.json
  rec-registry:
    openapi: http://rec:8000/openapi.json
"""


def _spec(version: str = "1.2.0") -> dict:
    return {"openapi": "3.1.0", "info": {"title": "t", "version": version}, "paths": {}}


# ---------------------------------------------------------------------------
# The manifest
# ---------------------------------------------------------------------------


class TestManifest:
    # @verifies REQ-0100
    def test_services_are_declared_in_one_file(self, tmp_path):
        path = tmp_path / "services.yaml"
        path.write_text(MANIFEST)
        manifest = load_manifest(path)
        assert set(manifest.services) == {"digital-twin", "rec-registry"}
        assert manifest.services["digital-twin"].package == "dt"
        assert manifest.services["rec-registry"].package is None

    # @verifies REQ-0100
    def test_a_document_that_is_not_a_mapping_is_refused(self, tmp_path):
        path = tmp_path / "services.yaml"
        path.write_text("- one\n")
        with pytest.raises(ValueError):
            load_manifest(path)

    # @verifies REQ-0100
    def test_a_service_without_a_spec_url_is_refused(self, tmp_path):
        path = tmp_path / "services.yaml"
        path.write_text("services:\n  dt:\n    package: dt\n")
        with pytest.raises(Exception):
            load_manifest(path)

    # @verifies REQ-0101
    @pytest.mark.parametrize(
        "name,override,expected",
        [
            ("rec-registry", None, "rec_registry"),
            ("digital-twin", "dt", "dt"),
            ("AI Assistant", None, "ai_assistant"),
            ("a--b", None, "a_b"),
            ("--", None, "service"),
            ("_leading_", None, "leading"),
        ],
    )
    def test_a_package_name_is_a_python_identifier(self, name, override, expected):
        assert package_slug(name, override) == expected


# ---------------------------------------------------------------------------
# Fetching and versioning
# ---------------------------------------------------------------------------


class TestSpecs:
    # @verifies REQ-0102
    def test_a_spec_is_accepted_as_json_or_yaml(self):
        as_json = json.dumps(_spec()).encode()
        assert parse_openapi_bytes(as_json)["info"]["version"] == "1.2.0"
        as_yaml = b"openapi: 3.1.0\ninfo:\n  version: '1.2.0'\n"
        assert parse_openapi_bytes(as_yaml)["info"]["version"] == "1.2.0"

    # @verifies REQ-0102
    def test_something_that_is_not_a_document_is_refused(self):
        with pytest.raises(ValueError):
            parse_openapi_bytes(b"- just\n- a list\n")

    # @verifies REQ-0103
    def test_a_spec_without_a_version_is_refused(self):
        with pytest.raises(ValueError, match="info.version"):
            spec_version({"info": {}})
        with pytest.raises(ValueError):
            spec_version({"info": {"version": ""}})
        with pytest.raises(ValueError):
            spec_version({})

    # @verifies REQ-0104
    def test_a_spec_is_stored_under_its_service_and_version(self, tmp_path):
        path = write_spec(tmp_path, "digital-twin", "1.2.0", _spec())
        assert path == tmp_path / "digital-twin" / "v1.2.0" / "openapi.json"
        assert json.loads(path.read_text())["info"]["version"] == "1.2.0"

    # @verifies REQ-0104
    def test_an_unchanged_spec_rewrites_byte_for_byte(self, tmp_path):
        """Sorted keys and a fixed indent: re-fetching an unchanged spec must
        produce no diff, or every fetch looks like a change.
        """
        first = write_spec(tmp_path, "dt", "1.0.0", _spec("1.0.0")).read_bytes()
        shuffled = {
            "paths": {},
            "info": {"version": "1.0.0", "title": "t"},
            "openapi": "3.1.0",
        }
        second = write_spec(tmp_path, "dt", "1.0.0", shuffled).read_bytes()
        assert first == second

    # @verifies REQ-0104
    def test_refetching_the_same_version_overwrites_it(self, tmp_path):
        """Pinned because the published documentation claimed the opposite. A
        service that changes its API without bumping `info.version` replaces the
        snapshot in place, and the diff is the only signal.
        """
        write_spec(tmp_path, "dt", "1.0.0", _spec("1.0.0"))
        changed = _spec("1.0.0")
        changed["paths"] = {"/new": {}}
        path = write_spec(tmp_path, "dt", "1.0.0", changed)
        assert "/new" in json.loads(path.read_text())["paths"]

    # @verifies REQ-0105
    def test_versions_are_discoverable(self, tmp_path):
        for version in ("1.0.0", "1.1.0", "2.0.0"):
            write_spec(tmp_path, "dt", version, _spec(version))
        assert list_versions(tmp_path, "dt") == ["v1.0.0", "v1.1.0", "v2.0.0"]
        assert latest_version(tmp_path, "dt") == "v2.0.0"

    # @verifies REQ-0105
    def test_an_unknown_service_has_no_versions(self, tmp_path):
        assert list_versions(tmp_path, "absent") == []
        assert latest_version(tmp_path, "absent") is None

    # @verifies REQ-0105
    def test_versions_are_ordered_by_number_not_by_character(self, tmp_path):
        """Character ordering put `v0.10.0` before `v0.2.0`, so "latest" was an
        older spec and generation used it silently.
        """
        for version in ("0.2.0", "0.10.0", "0.9.0"):
            write_spec(tmp_path, "dt", version, _spec(version))
        assert list_versions(tmp_path, "dt") == ["v0.2.0", "v0.9.0", "v0.10.0"]
        assert latest_version(tmp_path, "dt") == "v0.10.0"

    # @verifies REQ-0105
    def test_double_digit_components_order_at_every_position(self, tmp_path):
        for version in ("1.0.0", "10.0.0", "2.0.0", "2.0.10", "2.0.2"):
            write_spec(tmp_path, "dt", version, _spec(version))
        assert list_versions(tmp_path, "dt") == [
            "v1.0.0",
            "v2.0.0",
            "v2.0.2",
            "v2.0.10",
            "v10.0.0",
        ]

    # @verifies REQ-0105
    def test_a_non_numeric_version_still_orders(self, tmp_path):
        """Not semver — a total order over whatever a service puts in
        `info.version`. What matters is that it never raises and never loses a
        directory.
        """
        for version in ("1.0.0", "1.0.0-beta", "snapshot"):
            write_spec(tmp_path, "dt", version, _spec(version))
        ordered = list_versions(tmp_path, "dt")
        assert set(ordered) == {"v1.0.0", "v1.0.0-beta", "vsnapshot"}
        assert ordered.index("v1.0.0") < ordered.index("vsnapshot")

    # @verifies REQ-0106
    def test_one_services_failure_does_not_stop_the_others(self, tmp_path, monkeypatch):
        manifest = tmp_path / "services.yaml"
        manifest.write_text(MANIFEST)
        out = tmp_path / "openapi"

        def fake_fetch(url: str, timeout: float = 20.0) -> dict:
            if "rec" in url:
                raise RuntimeError("connection refused")
            return _spec()

        monkeypatch.setattr(spec_cli, "fetch_spec", fake_fetch)
        spec_cli.fetch(str(manifest), False, str(out))

        assert (out / "digital-twin" / "v1.2.0" / "openapi.json").exists()
        assert not (out / "rec-registry").exists()


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------


class TestGeneratedTreeMatchesTheManifest:
    """Asserted against this repository's own tree, not a fixture.

    Both halves of REQ-0114 fail silently in production: an orphaned package is
    simply never regenerated, and a service whose spec cannot be fetched is one
    reported line in a command nobody reads the output of.
    """

    @staticmethod
    def _repo_root() -> Path:
        return Path(__file__).resolve().parents[1]

    def _declared(self) -> set[str]:
        manifest = load_manifest(self._repo_root() / "services.yaml")
        return {
            package_slug(name, entry.package)
            for name, entry in manifest.services.items()
        }

    def _generated(self) -> set[str]:
        root = self._repo_root() / "src" / "celine" / "sdk" / "openapi"
        return {
            p.name
            for p in root.iterdir()
            if p.is_dir() and not p.name.startswith(("_", "."))
        }

    # @verifies REQ-0114
    def test_no_generated_package_is_missing(self):
        missing = self._declared() - self._generated()
        assert not missing, (
            f"declared in services.yaml but never generated: {sorted(missing)}. "
            "The usual cause is a spec URL the platform does not route — it "
            "answers 200 with an empty body, and the fetch skips it."
        )

    # @verifies REQ-0114
    def test_no_generated_package_is_orphaned(self):
        orphans = self._generated() - self._declared()
        assert not orphans, (
            f"generated but not in services.yaml: {sorted(orphans)}. Nothing "
            "regenerates these, so they are frozen while still looking current."
        )


class TestGeneration:
    # @verifies REQ-0107
    # @verifies REQ-0109
    def test_generation_reads_the_stored_specs(self, tmp_path, monkeypatch):
        manifest = tmp_path / "services.yaml"
        manifest.write_text(
            "services:\n  digital-twin:\n    package: dt\n"
            "    openapi: http://dt:8000/openapi.json\n"
        )
        specs = tmp_path / "openapi"
        write_spec(specs, "digital-twin", "1.0.0", _spec("1.0.0"))
        dest = tmp_path / "generated"
        (dest / "dt").mkdir(parents=True)
        (dest / "dt" / "stale.py").write_text("# a route that no longer exists")

        seen: list[Path] = []

        def fake_client(spec_path: Path, out_dir: Path, package_name: str) -> None:
            seen.append(spec_path)
            (out_dir / package_name).mkdir(parents=True)
            (out_dir / package_name / "__init__.py").write_text("# fresh")

        monkeypatch.setattr(generate_cli, "_generate_openapi_client", fake_client)
        monkeypatch.setattr(
            generate_cli, "_generate_openapi_schemas", lambda *a, **k: None
        )
        generate_cli.generate(str(manifest), str(specs), str(dest))

        assert seen == [specs / "digital-twin" / "v1.0.0" / "openapi.json"]
        assert (dest / "dt" / "__init__.py").read_text() == "# fresh"
        # Replaced wholesale: what upstream deleted is gone here too.
        assert not (dest / "dt" / "stale.py").exists()

    # @verifies REQ-0113
    def test_a_missing_generator_is_reported_as_a_broken_environment(
        self, monkeypatch, tmp_path
    ):
        """The generators are declared in this project's `dev` group, so one being
        absent means the environment is wrong — not that something needs
        installing by hand. The bare `FileNotFoundError` this replaces named the
        binary and nothing else.
        """

        def not_installed(*args, **kwargs):
            raise FileNotFoundError(2, "No such file or directory")

        monkeypatch.setattr(generate_cli.subprocess, "run", not_installed)

        with pytest.raises(RuntimeError) as exc:
            generate_cli._generate_openapi_client(tmp_path / "s.json", tmp_path, "dt")
        message = str(exc.value)
        assert "openapi-python-client" in message
        assert "pyproject.toml" in message  # where it is declared
        assert "3.11" in message  # the other way it goes missing
        assert "uv sync" in message  # how to put it back

        with pytest.raises(RuntimeError) as exc:
            generate_cli._generate_openapi_schemas(tmp_path / "s.json", tmp_path / "x.py")
        assert "datamodel-codegen" in str(exc.value)

    # @verifies REQ-0113
    def test_a_generator_that_runs_and_fails_still_reports_its_own_output(
        self, monkeypatch, tmp_path
    ):
        """The missing-binary path must not swallow the ordinary failure path: a
        generator that runs and rejects the spec still reports what it said.
        """
        import subprocess as real_subprocess

        def failed(*args, **kwargs):
            return real_subprocess.CompletedProcess(
                args=args, returncode=1, stdout="", stderr="unsupported schema"
            )

        monkeypatch.setattr(generate_cli.subprocess, "run", failed)
        with pytest.raises(RuntimeError, match="unsupported schema"):
            generate_cli._generate_openapi_client(tmp_path / "s.json", tmp_path, "dt")

    # @verifies REQ-0108
    def test_a_missing_spec_fails_loudly(self, tmp_path, monkeypatch):
        manifest = tmp_path / "services.yaml"
        manifest.write_text(
            "services:\n  digital-twin:\n    openapi: http://dt:8000/openapi.json\n"
        )
        called: list[str] = []
        monkeypatch.setattr(
            generate_cli,
            "_generate_openapi_client",
            lambda *a, **k: called.append("ran"),
        )
        with pytest.raises(RuntimeError, match="digital-twin"):
            generate_cli.generate(
                str(manifest), str(tmp_path / "openapi"), str(tmp_path / "out")
            )
        assert called == []


# ---------------------------------------------------------------------------
# The boundary around generated code
# ---------------------------------------------------------------------------


class _ClientModel:
    """Shaped like an openapi-python-client model."""

    def __init__(self, **data) -> None:
        self.data = data

    def to_dict(self) -> dict:
        return self.data

    @classmethod
    def from_dict(cls, src_dict: dict) -> "_ClientModel":
        return cls(**src_dict)


class _Schema(BaseModel):
    community_id: str = Field(alias="communityId")
    label: str | None = None


class TestConversion:
    # @verifies REQ-0110
    def test_a_generated_object_becomes_a_schema(self):
        schema = to_schema(_ClientModel(communityId="rec-1", label="A"), _Schema)
        assert schema.community_id == "rec-1"
        assert schema.label == "A"

    # @verifies REQ-0110
    def test_a_schema_becomes_a_generated_object(self):
        client = to_client(_Schema(communityId="rec-1", label="A"), _ClientModel)
        assert client.to_dict() == {"communityId": "rec-1", "label": "A"}

    # @verifies REQ-0110
    def test_none_survives_both_directions(self):
        """An optional field needs no branch at every call site — which is the
        whole reason services can hold typed models over a regenerated wire.
        """
        assert to_schema(None, _Schema) is None
        assert to_client(None, _ClientModel) is None

    # @verifies REQ-0111
    def test_converting_to_a_client_sends_only_what_was_set(self):
        """An omitted field must stay omitted rather than being transmitted as its
        default and overwriting a value on the server.
        """
        client = to_client(_Schema(communityId="rec-1"), _ClientModel)
        assert client.to_dict() == {"communityId": "rec-1"}


class TestUnwrap:
    # @verifies REQ-0112
    def test_a_parsed_response_is_returned(self):
        response = Response(
            status_code=HTTPStatus.OK, content=b"{}", headers={}, parsed={"ok": True}
        )
        assert unwrap(response) == {"ok": True}

    # @verifies REQ-0112
    def test_an_unparsed_response_carries_the_evidence(self):
        """The raw body is kept because a failed call's only diagnosis is usually
        what the service actually said.
        """
        response = Response(
            status_code=HTTPStatus.FORBIDDEN,
            content=b'{"detail":"not your community"}',
            headers={},
            parsed=None,
        )
        with pytest.raises(DTApiError) as exc:
            unwrap(response)
        assert exc.value.status_code == HTTPStatus.FORBIDDEN
        assert b"not your community" in exc.value.body

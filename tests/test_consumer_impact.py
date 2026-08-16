"""Tests for `scripts/consumer_impact.py` — docs/specifications/spec-management.md.

Both cases pinned here were live false positives before they were fixed, and
both are the kind that make a report untrustworthy rather than merely noisy: one
announced a breakage that did not exist, the other counted a repository that
vendors everyone else's code as a consumer of everything.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import consumer_impact as impact  # noqa: E402


class TestPublicNames:
    # @verifies REQ-0115
    def test_definitions_are_the_surface(self):
        source = "class Client: pass\ndef helper(): pass\nTOKEN = 1\n"
        assert impact._names(source, imports=False) == {"Client", "helper", "TOKEN"}

    # @verifies REQ-0115
    def test_private_names_are_not_the_surface(self):
        source = "class _Internal: pass\ndef _helper(): pass\n"
        assert impact._names(source, imports=False) == set()

    # @verifies REQ-0115
    def test_imports_are_not_definitions(self):
        """A module's stdlib imports vanishing with it is not a loss anyone can
        suffer, and listing them buries the names that matter.
        """
        source = "from typing import Any\nimport httpx\nclass Real: pass\n"
        assert impact._names(source, imports=False) == {"Real"}

    # @verifies REQ-0115
    def test_imports_are_available_for_the_removal_check(self):
        """The re-export case: a class that moves elsewhere and is imported back
        is still importable from here, so it must not read as removed.
        """
        source = "from celine.sdk.auth.models import AccessToken\n"
        assert impact._names(source, imports=False) == set()
        assert impact._names(source, imports=True) == {"AccessToken"}

    # @verifies REQ-0115
    def test_an_unparseable_module_yields_nothing_rather_than_raising(self):
        assert impact._names("def broken(:\n", imports=True) == set()


class TestVendoredCode:
    # @verifies REQ-0115
    @pytest.mark.parametrize(
        "relative",
        [
            ".work/nudging-tool/src/celine/nudging/auth.py",  # the docs site's checkouts
            ".venv/lib/python3.12/site-packages/celine/sdk/auth/jwt.py",
            "node_modules/thing/x.py",
            "build/lib/app.py",
            "src/app/__pycache__/auth.cpython-312.py",
        ],
    )
    def test_code_that_lives_here_without_belonging_here_is_excluded(self, relative):
        repo = Path("/w/repo")
        assert impact._vendored(repo / relative, repo)

    # @verifies REQ-0115
    def test_a_repositorys_own_code_is_not_excluded(self):
        repo = Path("/w/repo")
        for relative in ("src/app/auth.py", "tests/test_auth.py", "main.py"):
            assert not impact._vendored(repo / relative, repo)


class TestImportDetection:
    # @verifies REQ-0115
    @pytest.mark.parametrize(
        "line",
        [
            "from celine.sdk.auth import JwtUser",
            "from celine.sdk import settings",
            "import celine.sdk.broker",
            "    from celine.sdk.auth.jwt import extract_groups",  # inside a function
        ],
    )
    def test_an_import_marks_a_consumer(self, line):
        assert impact.IMPORTS_SDK.search(line)

    # @verifies REQ-0115
    @pytest.mark.parametrize(
        "line",
        [
            "# celine.sdk.auth is where tokens are verified",
            '"""Uses celine.sdk.settings for configuration."""',
            "url = 'https://example/celine.sdk'",
        ],
    )
    def test_a_mention_does_not(self, line):
        """Documentation and generator scripts name this package constantly
        without depending on it.
        """
        assert not impact.IMPORTS_SDK.search(line)


class TestImportedPairs:
    # @verifies REQ-0115
    def test_a_multiline_import_is_read_as_its_names(self, tmp_path):
        """Grepping would see this as nothing; the syntax sees three facts."""
        f = tmp_path / "consumer.py"
        f.write_text(
            "from celine.sdk.auth import (\n"
            "    JwtUser,\n"
            "    extract_groups,\n"
            ")\n"
            "import celine.sdk.broker\n"
        )
        assert impact.imported_pairs([f]) == {
            ("celine.sdk.auth", "JwtUser"),
            ("celine.sdk.auth", "extract_groups"),
            ("celine.sdk.broker", ""),
        }

    # @verifies REQ-0115
    def test_an_import_inside_a_function_still_counts(self, tmp_path):
        """A deferred import is a dependency that fails later, not less."""
        f = tmp_path / "consumer.py"
        f.write_text("def check():\n    from celine.sdk.policies import Decision\n")
        assert impact.imported_pairs([f]) == {("celine.sdk.policies", "Decision")}

    # @verifies REQ-0115
    def test_other_packages_are_ignored(self, tmp_path):
        f = tmp_path / "consumer.py"
        f.write_text("from celine.utils import thing\nimport httpx\n")
        assert impact.imported_pairs([f]) == set()


class TestResolution:
    # @verifies REQ-0115
    def test_what_exists_resolves(self):
        assert (
            impact.unresolved(
                {
                    ("celine.sdk.auth", "JwtUser"),
                    ("celine.sdk.settings", "PoliciesSettings"),
                    ("celine.sdk.broker", ""),
                }
            )
            == []
        )

    # @verifies REQ-0115
    def test_a_missing_name_is_reported_against_its_module(self):
        failures = impact.unresolved({("celine.sdk.auth", "TokenProviderThatNeverWas")})
        assert len(failures) == 1
        module, name, why = failures[0]
        assert (module, name) == ("celine.sdk.auth", "TokenProviderThatNeverWas")
        assert "not found" in why

    # @verifies REQ-0115
    def test_a_module_that_does_not_exist_is_reported_with_its_error(self):
        failures = impact.unresolved({("celine.sdk.nonexistent", "Thing")})
        assert len(failures) == 1
        assert "ModuleNotFoundError" in failures[0][2]


class TestModulePaths:
    # @verifies REQ-0115
    def test_a_source_path_becomes_a_module_path(self):
        assert impact._module_of("src/celine/sdk/auth/jwt.py") == "celine.sdk.auth.jwt"

    # @verifies REQ-0115
    def test_a_package_init_is_the_package(self):
        assert impact._module_of("src/celine/sdk/auth/__init__.py") == "celine.sdk.auth"

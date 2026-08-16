#!/usr/bin/env python3
"""Report which repositories a change to this SDK reaches.

This package is imported by most of the platform and tested by none of it: a
defect shipped from here arrives in a consumer on its next version bump, with no
file in that consumer changing. Nothing in this repository's own suite can see
that, so this script answers the one question it cannot — *who would notice?*

It reports three things, in increasing order of urgency:

1. **Reach** — which repositories import each module this change touched.
2. **Removed public names still imported somewhere** — a name that existed at the
   base revision, does not exist now, and is named by a consumer.
3. **Unresolved imports** — every `(module, name)` any consumer imports, checked
   against this SDK as it stands. This one does not care what changed or how,
   only whether what consumers ask for is still there, which is why it catches
   what a diff cannot: a name that moved between packages, a module that now
   fails at import time, a generated model that vanished in a regeneration.

Read-only: it clones nothing, installs nothing and writes nothing. The third
check imports this package, so run it under `uv run` in a checkout (or pass
`--no-resolve`).

    python scripts/consumer_impact.py                  # working tree vs HEAD
    python scripts/consumer_impact.py --since v1.15.0  # since a release
    python scripts/consumer_impact.py --json           # for a pipeline

Exit status is 1 when a consumer would break — a removed name still imported, or
an import that does not resolve — so it can gate a release; 0 otherwise,
including when there is simply nothing to report.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

SDK_ROOT = Path(__file__).resolve().parents[1]
SRC = SDK_ROOT / "src" / "celine" / "sdk"
# Consumers live beside this repository in the celine-dev workspace. Nothing
# outside it can be seen, which is stated in the report rather than assumed away.
WORKSPACE = SDK_ROOT.parent


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(SDK_ROOT), *args], capture_output=True, text=True
    )
    return result.stdout if result.returncode == 0 else ""


def _names(source: str, *, imports: bool) -> set[str]:
    """Top-level names in a module.

    Two readings, and the difference is what keeps this honest:

    - **defined** (`imports=False`) — what this module declares. This is what
      "removed" is measured against, so a module's stdlib imports never appear
      as a loss.
    - **available** (`imports=True`) — everything importable from it, including
      re-exports. A class that moves elsewhere and is re-exported here is still
      importable here, and calling that a removal would false-alarm on exactly
      the refactor most likely to be safe.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif imports and isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update(a.asname or a.name.split(".")[0] for a in node.names)
    return {n for n in names if not n.startswith("_")}


def _module_of(path: str) -> str:
    """`src/celine/sdk/auth/jwt.py` -> `celine.sdk.auth.jwt`."""
    rel = Path(path).relative_to("src")
    parts = list(rel.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def changed(since: str) -> tuple[dict[str, set[str]], set[str]]:
    """Return (modules touched -> removed public names, all touched top modules)."""
    removed: dict[str, set[str]] = {}
    touched: set[str] = set()

    status = _git("diff", "--name-status", since, "--", "src/celine/sdk")
    for line in status.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        state, path = parts[0], parts[-1]
        if not path.endswith(".py"):
            continue
        module = _module_of(path)
        touched.add(".".join(module.split(".")[:3]))  # celine.sdk.<module>

        before = _names(_git("show", f"{since}:{path}"), imports=False)
        after: set[str] = set()
        if state != "D" and (SDK_ROOT / path).exists():
            after = _names(
                (SDK_ROOT / path).read_text(encoding="utf-8"), imports=True
            )
        gone = before - after
        if gone:
            removed[module] = gone
    return removed, touched


# An *import*, not a mention. Documentation and generator scripts talk about
# `celine.sdk` constantly without depending on it, and counting those as
# consumers inflates every number in this report.
IMPORTS_SDK = re.compile(
    r"^\s*(?:from\s+celine\.sdk[\w.]*\s+import|import\s+celine\.sdk)", re.MULTILINE
)


VENDORED = {"node_modules", "build", "dist", "site-packages", "__pycache__"}


def _vendored(path: Path, repo: Path) -> bool:
    """Code that lives in a repository without belonging to it.

    Dot-directories are the load-bearing half: the documentation site keeps
    **checkouts of every other repository** under `.work/` so its build can read
    their docs. Counted naively, that one repository appears to import
    everything, and every other repository's usage is double-counted through it.
    """
    parts = path.relative_to(repo).parts
    return any(p.startswith(".") or p in VENDORED for p in parts)


def consumers() -> dict[str, list[Path]]:
    """Every sibling repository, with the Python files that import this SDK."""
    found: dict[str, list[Path]] = {}
    for repo in sorted(WORKSPACE.iterdir()):
        if not repo.is_dir() or repo.resolve() == SDK_ROOT.resolve():
            continue
        if not (repo / ".git").exists():
            continue
        hits = [
            f
            for f in repo.rglob("*.py")
            if not _vendored(f, repo) and IMPORTS_SDK.search(_read(f))
        ]
        if hits:
            found[repo.name] = hits
    return found


_CACHE: dict[Path, str] = {}


def _read(path: Path) -> str:
    if path not in _CACHE:
        try:
            _CACHE[path] = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            _CACHE[path] = ""
    return _CACHE[path]


def reach(files: list[Path], module: str) -> bool:
    return module in "".join(_read(f) for f in files)


def imported_pairs(files: list[Path]) -> set[tuple[str, str]]:
    """Every `(module, name)` a consumer imports from this SDK.

    Read from the syntax rather than by grepping, so `from celine.sdk.auth
    import (JwtUser, extract_groups)` across three lines is one fact, not none.
    """
    pairs: set[tuple[str, str]] = set()
    for f in files:
        try:
            tree = ast.parse(_read(f))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("celine.sdk"):
                    pairs.update((node.module, a.name) for a in node.names)
            elif isinstance(node, ast.Import):
                pairs.update(
                    (a.name, "") for a in node.names if a.name.startswith("celine.sdk")
                )
    return pairs


def unresolved(pairs: set[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """Imports that do not resolve against the SDK as it stands now.

    This is the decisive check and the reason the diff-based one above is only a
    first pass: it does not care what changed or how, only whether what
    consumers ask for is still there. It needs this package importable, which it
    is under `uv run` in a checkout.
    """
    failures: list[tuple[str, str, str]] = []
    for module, name in sorted(pairs):
        try:
            mod = importlib.import_module(module)
        except Exception as exc:  # ImportError, or anything a module does at import
            failures.append((module, name, f"{type(exc).__name__}: {exc}"))
            continue
        if name and name != "*" and not hasattr(mod, name):
            failures.append((module, name, "name not found in module"))
    return failures


def breakages(
    files: list[Path], removed: dict[str, set[str]]
) -> list[tuple[str, str, Path]]:
    """Consumer files naming something this change removed."""
    out: list[tuple[str, str, Path]] = []
    for module, names in removed.items():
        for name in names:
            # A bare name is ambiguous, so require it to appear beside an import
            # of the module that lost it, or as a dotted access on it.
            pattern = re.compile(
                rf"(from\s+{re.escape(module)}\s+import[^\n]*\b{re.escape(name)}\b"
                rf"|{re.escape(module)}\.{re.escape(name)}\b)"
            )
            for f in files:
                if pattern.search(_read(f)):
                    out.append((module, name, f))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since",
        default="HEAD",
        help="base revision to compare against (default: HEAD, i.e. the working tree)",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--no-resolve",
        action="store_true",
        help="skip resolving consumer imports (which needs this package importable)",
    )
    args = parser.parse_args()

    removed, touched = changed(args.since)
    found = consumers()

    report: dict[str, object] = {
        "since": args.since,
        "workspace": str(WORKSPACE),
        "modules_touched": sorted(touched),
        "removed_public_names": {m: sorted(n) for m, n in removed.items()},
        "reach": {},
        "breakages": [],
        "unresolved": [],
    }

    for module in sorted(touched):
        report["reach"][module] = sorted(
            repo for repo, files in found.items() if reach(files, module)
        )

    for repo, files in sorted(found.items()):
        for module, name, path in breakages(files, removed):
            report["breakages"].append(
                {
                    "repository": repo,
                    "module": module,
                    "name": name,
                    "file": str(path.relative_to(WORKSPACE)),
                }
            )

    pairs: set[tuple[str, str]] = set()
    for files in found.values():
        pairs |= imported_pairs(files)
    report["imports_checked"] = len(pairs)
    if not args.no_resolve:
        report["unresolved"] = [
            {"module": m, "name": n, "why": why} for m, n, why in unresolved(pairs)
        ]

    failed = bool(report["breakages"] or report["unresolved"])

    if args.json:
        print(json.dumps(report, indent=2))
        return 1 if failed else 0

    print(f"Consumer impact of the change since {args.since}")
    print(f"  workspace: {WORKSPACE}  ({len(found)} repositories import this SDK)\n")

    if not touched:
        print("  nothing under src/celine/sdk changed — no reach to report.")
        return 0

    print("Reach — repositories importing each module this change touched:\n")
    for module, repos in report["reach"].items():
        listed = ", ".join(repos) if repos else "— nobody"
        print(f"  {module:<32} {len(repos):>2}  {listed}")

    if removed:
        print("\nPublic names this change removed:\n")
        for module, names in sorted(removed.items()):
            print(f"  {module}: {', '.join(sorted(names))}")

    if report["breakages"]:
        print("\n!! REMOVED NAMES STILL IMPORTED — these consumers break:\n")
        for b in report["breakages"]:
            print(f"  {b['repository']}: {b['name']} from {b['module']}")
            print(f"      {b['file']}")
    elif removed:
        print("\n  No consumer names any removed symbol.")

    if not args.no_resolve:
        checked = report["imports_checked"]
        if report["unresolved"]:
            print(
                f"\n!! UNRESOLVED IMPORTS — of {checked} distinct imports across "
                "the workspace, these do not exist here:\n"
            )
            for u in report["unresolved"]:
                dotted = f"{u['module']}.{u['name']}" if u["name"] else u["module"]
                print(f"  {dotted}  ({u['why']})")
        else:
            print(
                f"\n  All {checked} distinct imports across the workspace resolve "
                "against this working tree."
            )

    if failed:
        return 1

    print(
        "\nThis is a static read. It cannot see a consumer outside this workspace,\n"
        "a name reached by getattr, or a behaviour change that keeps its signature.\n"
        "For those: task dev:link, then run the consumer's own suite."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

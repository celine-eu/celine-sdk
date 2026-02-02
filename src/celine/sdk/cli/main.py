from __future__ import annotations

import typer

from celine.sdk.cli.spec import spec_app
from celine.sdk.cli.generate import gen_app


def create_app():
    app = typer.Typer(add_completion=True, help="CELINE SDK tooling")
    app.add_typer(spec_app, name="spec")
    app.add_typer(gen_app, name="generate")
    app()


if __name__ == "__main__":
    app = create_app()

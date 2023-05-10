from pathlib import Path
from typing import List, Optional

import typer

from get_it_done import ERRORS, __app_name__, __version__, config, database, get_it_done

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="get-it-done database location?",
    ),
) -> None:
    """Init the database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'creating config file with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'creating config file with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"database is {db_path}", fg=typer.colors.GREEN)
        
def _version_callback(value: bool) -> None:
    """Shows app version."""
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

def get_todoer() -> get_it_done.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'config file not found, run get-it-don init',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return get_it_done.Todoer(db_path)
    else:
        typer.secho(
            "DB not found, run get-it-don init ",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "--v",
        help="Show the apps version",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

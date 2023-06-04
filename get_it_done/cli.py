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

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a description."""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to-do failed with"{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN
        )

@app.command(name="list")
def list_items() -> None:
    """List all items in db."""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    if len(todo_list) == 0:
        typer.secho(
            'No items found',
            fg=typer.colors.RED,
        )
        raise typer.Exit()
    typer.secho("\nto-do list:\n",
                fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID. ",
        "| Priority ",
        "| Done ",
        "| Description ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.GREEN, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.GREEN)
    for id, todo in enumerate(todo_list, 1):
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.GREEN,
        )
        typer.secho("-" * len(headers) + "\n", fg=typer.colors.GREEN)

        
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

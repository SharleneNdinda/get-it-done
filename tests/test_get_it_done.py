import json

import pytest
from typer.testing import CliRunner

from get_it_done import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__, 
    __version__,
    cli, 
    get_it_done
)
from . import data

runner = CliRunner()

@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{
        "Description": "Get milk", 
        "Priority": 2,
        "Done": False
    }]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

def test_version():
    """Test the app version."""
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.mark.parametrize(
    "description, priority, expected",
    [
        pytest.param(
            data.test_data["description"],
            data.test_data["priority"],
            (data.test_data["todo"], SUCCESS),
        ),
        pytest.param(
            data.test_data2["description"],
            data.test_data2["priority"],
            (data.test_data2["todo"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):
    todo = get_it_done.Todoer(mock_json_file)
    assert todo.add(description, priority) == expected
    read = todo._db_handler.read_todos()
    assert len(read.todo_list) == 2
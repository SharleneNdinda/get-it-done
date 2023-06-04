from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from get_it_done.database import DatabaseHandler
from get_it_done import DB_READ_ERROR


class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, descritpion: List[str], priority: int = 2) -> CurrentTodo:
        """Add a new to-do to the database."""
        descritpion_text = " ".join(descritpion)
        if not descritpion_text.endswith("."):
            descritpion_text += "."
        todo = {
            "Description": descritpion_text,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)
    
    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return todo list."""
        read = self._db_handler.read_todos()
        return read.todo_list

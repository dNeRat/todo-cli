from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from todo.model import Task


def get_db_path() -> Path:
    """
    Хочу, чтобы json лежал с main.py
    Возвращает путь к tasks.json в корне проекта (рядом с main.py)
    """
    # storage.py лежит в todo/storage.py
    # parent - todo
    # parent - корень проекта (todo_cli)
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "tasks.json"


def load_tasks() -> list[Task]:
    db_path = get_db_path()

    if not db_path.exists():
        return []

    try:
        raw = db_path.read_text(encoding="utf-8")
        data = json.loads(raw)

        if not isinstance(data, list):
            raise ValueError("json ne list")

        tasks: list[Task] = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("item ne dict")
            tasks.append(Task(**item))

        return tasks

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        raise RuntimeError(f"tasks.json ne valid, format: {e}") from e


def save_tasks(tasks: list[Task]) -> None:
    db_path = get_db_path()

    data = [asdict(t) for t in tasks]
    text = json.dumps(data, ensure_ascii=False, indent=2)

    db_path.write_text(text, encoding="utf-8")
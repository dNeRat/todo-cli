from __future__ import annotations

import sys

from todo.model import Task
from todo.storage import load_tasks, save_tasks


def usage() -> None:
    print(
        "To-Do CLI\n"
        "Команды:\n"
        "   добавить таску  add \"текст\"\n"
        "   показать таски  list \n"
        "   отметить выполненной  done ID\n"
        "   удалить  rm ID \n"
        "   удалить все выполненные  clear \n"
        "\n"
        "Примеры:\n"
        "  py main.py add \"выгулять кота\"\n"
        "  py main.py list\n"
        "  py main.py done 1\n"
        "  py main.py rm 1\n"
        "  py main.py clear\n"
    )


def next_id(tasks: list[Task]) -> int:
    return max((t.id for t in tasks), default=0) + 1


def cmd_add(tasks: list[Task], text: str) -> None:
    text = text.strip()
    if not text:
        print("текст таски пуст", file=sys.stderr)
        sys.exit(1)

    t = Task(id=next_id(tasks), text=text, done=False)
    tasks.append(t)
    save_tasks(tasks)
    print(f"add: [{t.id}] {t.text}")


def cmd_list(tasks: list[Task]) -> None:
    if not tasks:
        print("список пуст")
        return

    # Сначала невыполненные (done=False), потом выполненные (done=True), и по id
    ordered = sorted(tasks, key=lambda t: (t.done, t.id))

    for t in ordered:
        mark = "+" if t.done else " "
        print(f"[{t.id:03d}] [{mark}] {t.text}")


def _parse_id(value: str) -> int:
    try:
        task_id = int(value)
    except ValueError:
        print("id ne int", file=sys.stderr)
        sys.exit(1)

    if task_id <= 0:
        print("pzdc", file=sys.stderr)
        sys.exit(1)

    return task_id


def cmd_done(tasks: list[Task], task_id: int) -> None:
    for t in tasks:
        if t.id == task_id:
            if t.done:
                print(f"task [{task_id}] already done")
                return
            t.done = True
            save_tasks(tasks)
            print(f"done [{task_id}] {t.text}")
            return

    print(f"net zadachi s id={task_id}", file=sys.stderr)
    sys.exit(1)


def cmd_rm(tasks: list[Task], task_id: int) -> None:
    new_tasks = [t for t in tasks if t.id != task_id]
    if len(new_tasks) == len(tasks):
        print(f"net zadachi s id={task_id}", file=sys.stderr)
        sys.exit(1)

    save_tasks(new_tasks)
    print(f"del: [{task_id}]")

def cmd_clear(tasks: list[Task]) -> None:
    """
    Удаляет все выполненные задачи
    """
    remaining = [t for t in tasks if not t.done]
    removed = len(tasks) - len(remaining)

    if removed == 0:
        print("Нет выполненных задач, нечего очищать")
        return

    save_tasks(remaining)
    print(f"Удалено выполненных задач: {removed}")


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        usage()
        return

    cmd = argv[1].lower()
    tasks = load_tasks()

    if cmd == "add":
        if len(argv) < 3:
            print("text", file=sys.stderr)
            sys.exit(1)
        text = " ".join(argv[2:])  # чтобы работало без кавычек тоже
        cmd_add(tasks, text)

    elif cmd == "list":
        cmd_list(tasks)

    elif cmd == "clear":
        cmd_clear(tasks)

    elif cmd == "done":
        if len(argv) != 3:
            print("id nado", file=sys.stderr)
            sys.exit(1)
        task_id = _parse_id(argv[2])
        cmd_done(tasks, task_id)

    elif cmd == "rm":
        if len(argv) != 3:
            print("id nado", file=sys.stderr)
            sys.exit(1)
        task_id = _parse_id(argv[2])
        cmd_rm(tasks, task_id)

    else:
        print(f"neponimeow {cmd}", file=sys.stderr)
        usage()
        sys.exit(1)
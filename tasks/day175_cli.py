```python
import argparse
from typing import Optional
from project_final.core import TaskManager

def parse_args():
    parser = argparse.ArgumentParser(description="CLI para gerenciamento de tarefas no projeto_final")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando: list
    list_parser = subparsers.add_parser("list", help="Listar todas as tarefas")
    list_parser.add_argument("--status", type=str, help="Filtrar por status (ex: 'pending', 'completed')")

    # Comando: add
    add_parser = subparsers.add_parser("add", help="Adicionar nova tarefa")
    add_parser.add_argument("title", type=str, help="Título da tarefa")
    add_parser.add_argument("--description", type=str, default="", help="Descrição da tarefa")
    add_parser.add_argument("--status", type=str, default="pending", help="Status inicial (default: 'pending')")

    # Comando: update
    update_parser = subparsers.add_parser("update", help="Atualizar tarefa existente")
    update_parser.add_argument("task_id", type=int, help="ID da tarefa")
    update_parser.add_argument("--title", type=str, help="Novo título")
    update_parser.add_argument("--description", type=str, help="Nova descrição")
    update_parser.add_argument("--status", type=str, help="Novo status")

    # Comando: delete
    delete_parser = subparsers.add_parser("delete", help="Remover tarefa")
    delete_parser.add_argument("task_id", type=int, help="ID da tarefa")

    return parser.parse_args()

def main():
    args = parse_args()
    task_manager = TaskManager()

    if args.command == "list":
        tasks = task_manager.list_tasks(status=args.status)
        for task in tasks:
            print(f"ID: {task.id}, Título: {task.title}, Status: {task.status}")

    elif args.command == "add":
        task = task_manager.add_task(
            title=args.title,
            description=args.description,
            status=args.status
        )
        print(f"Tarefa adicionada com ID: {task.id}")

    elif args.command == "update":
        task_manager.update_task(
            task_id=args.task_id,
            title=args.title,
            description=args.description,
            status=args.status
        )
        print(f"Tarefa {args.task_id} atualizada")

    elif args.command == "delete":
        task_manager.delete_task(task_id=args.task_id)
        print(f"Tarefa {args.task_id} removida")

if __name__ == "__main__":
    main()
```
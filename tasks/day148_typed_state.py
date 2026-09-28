```python
from typing import TypedDict, List, Optional
from langgraph.graph import Graph

class TaskState(TypedDict):
    task_id: str
    description: str
    status: str  # "pending", "in_progress", "completed"
    assignee: Optional[str]
    dependencies: List[str]

def create_task_graph() -> Graph:
    workflow = Graph()

    def add_task_node(state: TaskState) -> TaskState:
        print(f"Adicionando tarefa: {state['description']}")
        return state

    def update_status_node(state: TaskState) -> TaskState:
        print(f"Atualizando status da tarefa {state['task_id']} para {state['status']}")
        return state

    workflow.add_node("add_task", add_task_node)
    workflow.add_node("update_status", update_status_node)

    workflow.set_entry_point("add_task")
    workflow.add_edge("add_task", "update_status")

    return workflow

# Exemplo de uso
if __name__ == "__main__":
    graph = create_task_graph()

    initial_state: TaskState = {
        "task_id": "task_001",
        "description": "Implementar feature X",
        "status": "pending",
        "assignee": "dev1",
        "dependencies": []
    }

    graph.run(initial_state)
```
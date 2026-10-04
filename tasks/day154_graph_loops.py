```python
from langgraph.graph import Graph
from langgraph.prebuilt import ToolNode
from typing import Annotated

# Definição de nós (tasks)
def task_a(state: Annotated[dict, "Estado atual"]):
    print("Executando Task A")
    state["steps"].append("A")
    return state

def task_b(state: Annotated[dict, "Estado atual"]):
    print("Executando Task B")
    state["steps"].append("B")
    return state

def task_c(state: Annotated[dict, "Estado atual"]):
    print("Executando Task C")
    state["steps"].append("C")
    return state

def check_condition(state: Annotated[dict, "Estado atual"]):
    print("Verificando condição...")
    return "loop" if len(state.get("steps", [])) < 5 else "end"

# Construção do grafo com loop
workflow = Graph()

# Adiciona nós
workflow.add_node("task_a", task_a)
workflow.add_node("task_b", task_b)
workflow.add_node("task_c", task_c)
workflow.add_node("check_condition", check_condition)
workflow.add_node("tools", ToolNode([task_a, task_b, task_c]))  # Nó para ferramentas

# Define fluxo principal
workflow.add_edge("__start__", "task_a")
workflow.add_edge("task_a", "task_b")
workflow.add_edge("task_b", "task_c")
workflow.add_edge("task_c", "check_condition")

# Adiciona loop condicional
workflow.add_conditional_edges(
    "check_condition",
    lambda state: state["next"] if "next" in state else "loop",
    {
        "loop": "task_a",  # Volta para task_a se condição for verdadeira
        "end": "__end__",  # Termina o fluxo
    }
)

# Configura estado inicial
app = workflow.compile()

# Executa o grafo com estado inicial
result = app.invoke({"steps": [], "next": None})
print("Resultado final:", result)
```
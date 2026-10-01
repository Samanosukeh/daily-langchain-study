```python
from langgraph.graph import Graph
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Definindo estado do grafo
class State(TypedDict):
    messages: Annotated[list, ...]
    task_status: str  # "pending", "in_progress", "completed", "failed"

# Função para verificar condição e decidir próximo passo
def check_condition_and_route(state: State):
    if state["task_status"] == "completed":
        return "end"
    elif state["task_status"] == "failed":
        return "handle_failure"
    else:
        return "continue_task"

# Função para simular tarefa
def execute_task(state: State):
    # Simula execução da tarefa
    print(f"Executando tarefa... Status atual: {state['task_status']}")

    # Atualiza status baseado em alguma lógica
    if "sucesso" in state["messages"][-1].content.lower():
        state["task_status"] = "completed"
    else:
        state["task_status"] = "failed"

    return state

# Função para lidar com falha
def handle_failure(state: State):
    print("Tarefa falhou! Tentando recuperar...")
    state["task_status"] = "pending"  # Reinicia para tentar novamente
    return state

# Configuração do grafo
workflow = Graph()

# Adiciona nós
workflow.add_node("start", lambda state: state)  # Nó inicial
workflow.add_node("execute_task", execute_task)
workflow.add_node("handle_failure", handle_failure)
workflow.add_node("end", lambda state: {"result": "Tarefa concluída com sucesso!"})

# Adiciona edges condicionais
workflow.add_edge("start", "execute_task")
workflow.add_conditional_edges(
    "execute_task",
    check_condition_and_route,
    {
        "continue_task": "execute_task",
        "end": "end",
        "handle_failure": "handle_failure"
    }
)
workflow.add_edge("handle_failure", "execute_task")  # Loop de recuperação
workflow.add_edge("end", END)  # Nó final

# Compila o grafo
app = workflow.compile()

# Execução de exemplo
initial_state = {
    "messages": [HumanMessage(content="Iniciar tarefa crítica")],
    "task_status": "pending"
}

result = app.invoke(initial_state)
print(result)
```
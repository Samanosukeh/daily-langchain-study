```python
from langgraph.graph import Graph
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from typing import Annotated, Literal

# Ferramentas para o agente
@tool
def search_web(query: str) -> str:
    """Busca informações na web com base na query."""
    # Implementação fictícia
    return f"Resultado da busca para: {query}"

@tool
def calculator(expression: str) -> float:
    """Calcula expressões matemáticas."""
    # Implementação fictícia
    return eval(expression)

# Nó de decisão para ReAct
def react_decision(state: list) -> Literal["action", "finish"]:
    """Decide se o agente deve agir ou finalizar."""
    last_message = state[-1]
    if "Action:" in last_message.content:
        return "action"
    return "finish"

# Nó de ação
def react_action(state: list) -> dict:
    """Extrai a ação e argumentos do último message."""
    last_message = state[-1]
    content = last_message.content

    # Extração simplificada (melhorar com parser robusto)
    if "Action:" in content and "Action Input:" in content:
        action = content.split("Action:")[1].split("Action Input:")[0].strip()
        input_data = content.split("Action Input:")[1].strip()
        return {"tool": action, "tool_input": input_data}
    return {"tool": None, "tool_input": None}

# Nó de execução da ferramenta
def react_tool_execution(state: list) -> list:
    """Executa a ferramenta com os argumentos extraídos."""
    last_message = state[-1]
    if "tool" in last_message.additional_kwargs:
        tool_name = last_message.additional_kwargs["tool"]
        tool_input = last_message.additional_kwargs["tool_input"]

        # Seleciona a ferramenta
        tools = {"search_web": search_web, "calculator": calculator}
        tool_func = tools.get(tool_name)

        if tool_func:
            result = tool_func.invoke(tool_input)
            return [HumanMessage(content=f"Observação: {result}")]
    return []

# Construção do grafo
workflow = Graph()

# Adiciona nós
workflow.add_node("decision", react_decision)
workflow.add_node("action", react_action)
workflow.add_node("tools", ToolNode([search_web, calculator]))
workflow.add_node("tool_execution", react_tool_execution)

# Adiciona edges
workflow.add_edge("decision", "action")
workflow.add_edge("action", "tools")
workflow.add_edge("tools", "tool_execution")
workflow.add_edge("tool_execution", "decision")

# Configuração do loop condicional
workflow.add_conditional_edges(
    "decision",
    lambda state: "finish" if state == "finish" else "action",
    {"action": "action", "finish": END}
)

# Compila o grafo
app = workflow.compile()

# Exemplo de execução
if __name__ == "__main__":
    initial_message = HumanMessage(
        content="Quanto é 10 + 20? Busque também na web sobre LangGraph."
    )
    result = app.invoke(initial_message)
    print(result)
```
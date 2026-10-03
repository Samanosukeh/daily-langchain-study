```python
import pytest
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

def test_edge_condicional_roteia_para_no_correto():
    # Define o grafo com nós e condicionais
    workflow = StateGraph(dict)

    # Adiciona nós básicos
    workflow.add_node("node_a", lambda state: {"result": "A"})
    workflow.add_node("node_b", lambda state: {"result": "B"})

    # Define condicional que roteia para node_a ou node_b
    def router(state):
        return "node_a" if state.get("value", 0) < 10 else "node_b"

    # Adiciona edge condicional
    workflow.add_conditional_edges(
        "start",
        router,
        {"node_a": "node_a", "node_b": "node_b"}
    )

    # Define nó final
    workflow.add_node("end", lambda state: state)
    workflow.add_edge("node_a", "end")
    workflow.add_edge("node_b", "end")

    # Compila o grafo
    app = workflow.compile()

    # Teste 1: Valor menor que 10 deve rotear para node_a
    result = app.invoke({"value": 5})
    assert result["result"] == "A"

    # Teste 2: Valor maior ou igual a 10 deve rotear para node_b
    result = app.invoke({"value": 15})
    assert result["result"] == "B"

    # Teste 3: Valor ausente deve rotear para node_b (padrão)
    result = app.invoke({})
    assert result["result"] == "B"

def test_edge_condicional_com_toolnode():
    # Define o grafo com ToolNode
    workflow = StateGraph(dict)

    # Adiciona nós com ToolNode
    workflow.add_node("tool_a", ToolNode(["funcao_a"]))
    workflow.add_node("tool_b", ToolNode(["funcao_b"]))

    # Define condicional que roteia para tool_a ou tool_b
    def router(state):
        return "tool_a" if state.get("opcao") == "a" else "tool_b"

    # Adiciona edge condicional
    workflow.add_conditional_edges(
        "start",
        router,
        {"tool_a": "tool_a", "tool_b": "tool_b"}
    )

    # Define nó final
    workflow.add_node("end", lambda state: state)
    workflow.add_edge("tool_a", "end")
    workflow.add_edge("tool_b", "end")

    # Compila o grafo
    app = workflow.compile()

    # Teste 1: Opção 'a' deve rotear para tool_a
    result = app.invoke({"opcao": "a"})
    assert "tool_a" in result

    # Teste 2: Qualquer outra opção deve rotear para tool_b
    result = app.invoke({"opcao": "b"})
    assert "tool_b" in result

def test_edge_condicional_com_varios_destinos():
    # Define o grafo com múltiplos destinos
    workflow = StateGraph(dict)

    # Adiciona nós
    workflow.add_node("node_x", lambda state: {"result": "X"})
    workflow.add_node("node_y", lambda state: {"result": "Y"})
    workflow.add_node("node_z", lambda state: {"result": "Z"})

    # Define condicional com múltiplos destinos
    def router(state):
        valor = state.get("valor", 0)
        if valor < 5:
            return "node_x"
        elif 5 <= valor < 10:
            return "node_y"
        else:
            return "node_z"

    # Adiciona edge condicional
    workflow.add_conditional_edges(
        "start",
        router,
        {
            "node_x": "node_x",
            "node_y": "node_y",
            "node_z": "node_z"
        }
    )

    # Define nó final
    workflow.add_node("end", lambda state: state)
    workflow.add_edge("node_x", "end")
    workflow.add_edge("node_y", "end")
    workflow.add_edge("node_z", "end")

    # Compila o grafo
    app = workflow.compile()

    # Teste 1: Valor < 5 deve rotear para node_x
    result = app.invoke({"valor": 3})
    assert result["result"] == "X"

    # Teste 2: Valor entre 5 e 10 deve rotear para node_y
    result = app.invoke({"valor": 7})
    assert result["result"] == "Y"

    # Teste 3: Valor >= 1
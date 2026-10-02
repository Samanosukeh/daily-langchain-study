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

---

```markdown
# Comentários Detalhados no Grafo Condicional

## Introdução
No **LangGraph**, a execução de fluxos de trabalho pode ser modelada como um **grafo condicional**, onde nós (nodes) representam etapas de processamento e arestas (edges) definem as condições para transição entre eles. Comentários detalhados ajudam a documentar lógica complexa, facilitar a manutenção e depurar fluxos.

---

## Estrutura Básica de um Grafo Condicional

```python
from langgraph.graph import Graph

# Definição do grafo
workflow = Graph()

# Adicionar nós (nodes)
workflow.add_node("node1", funcao_node1)  # Função executada no nó
workflow.add_node("node2", funcao_node2)

# Adicionar arestas condicionais
workflow.add_conditional_edges(
    "node1",
    condicional_node1,
    {
        "next": "node2",  # Transição se condição for True
        "fallback": "node3"  # Transição se condição for False
    }
)

# Compilar o grafo
app = workflow.compile()
```

---

## Comentários em Nós e Arestas

### 1. **Comentários em Funções de Nó**
Documente o propósito da função, parâmetros esperados e comportamento.

```python
def funcao_node1(state: dict) -> dict:
    """
    Processa a entrada inicial e extrai entidades relevantes.

    Args:
        state (dict): Estado atual do grafo, contendo:
            - "input": Texto de entrada do usuário.
            - "entities": Lista de entidades extraídas (inicialmente vazia).

    Returns:
        dict: Estado atualizado com entidades extraídas.
    """
    texto = state["input"]
    entidades = extrair_entidades(texto)  # Função hipotética
    return {"entities": entidades, **state}
```

---

### 2. **Comentários em Funções Condicionais**
Documente a lógica de decisão e casos de borda.

```python
def condicional_node1(state: dict) -> str:
    """
    Determina a próxima etapa com base no estado atual.

    Regras:
        - Se "entities" não estiver vazio: avança para "node2".
        - Caso contrário: encaminha para "node3" para tratamento de erro.

    Args:
        state (dict): Estado atual do grafo.

    Returns:
        str: Nome do próximo nó ("next" ou "fallback").
    """
    if state.get("entities"):
        return "next"
    return "fallback"
```

---

### 3. **Comentários em Arestas Condicionais**
Documente as condições e transições.

```python
workflow.add_conditional_edges(
    "node1",
    condicional_node1,
    {
        # Avança para node2 se entidades forem extraídas
        "next": "node2",

        # Trata falha na extração de entidades
        "fallback": "node3"
    }
)
```

---

## Boas Práticas para Comentários

### 1. **Clareza na Lógica**
- Documente **por que** uma condição existe, não apenas **o que** ela faz.
- Exemplo:
  ```python
  # Verifica se o texto contém perguntas diretas (ex: "Como fazer X?")
  # para rotear para o nó de resposta específica.
  ```

### 2. **Casos de Borda**
- Comente como o sistema lida com entradas inesperadas.
  ```python
  # Se o texto estiver vazio, encaminha para node_vazio.
  ```

### 3. **Estado Esperado**
- Descreva a estrutura do `state` em cada nó.
  ```python
  # Estado esperado:
  # {
  #   "input": str,  # Texto do usuário
  #   "entities": list,  # Entidades extraídas
  #   "historico": list  # Histórico de interações
  # }
  ```

### 4. **Depuração**
- Adicione comentários para pontos críticos de depuração.
  ```python
  # LOG: Estado antes da extração de entidades
  logger.debug(f"Estado inicial: {state}")
  ```

---

## Exemplo Completo com Comentários

```python
from langgraph.graph import Graph
import logging

logger = logging.getLogger(__name__)

def extrair_entidades(texto: str) -> list:
    """Extrai entidades do texto usando NLP."""
    # Implementação omitida
    pass

def node1(state: dict) -> dict:
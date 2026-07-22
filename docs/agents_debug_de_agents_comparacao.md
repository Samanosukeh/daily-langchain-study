```markdown
# Debug de Agents: Interpretando Traces em LangChain vs. LangGraph

## **LangChain (Abordagem Tradicional)**
- **Trace simples**: Exibe logs lineares com `LCEL` (LangChain Expression Language).
  ```python
  from langchain_core.tracers import ConsoleCallbackHandler
  chain.invoke({"input": "Pergunta"}, config={"callbacks": [ConsoleCallbackHandler()]})
  ```
- **Saída típica**:
  ```
  [chain/start] Entering Chain run with input: {'input': 'Pergunta'}
  [llm/start] Entering LLM run...
  [llm/end] Finished LLM run. Output: "Resposta"
  [chain/end] Finished Chain run.
  ```
- **Limitações**:
  - Falta de hierarquia clara entre nós.
  - Dificuldade em rastrear loops ou dependências complexas.
  - Verbosidade em agentes com múltiplas ferramentas.

---

## **LangGraph (Abordagem Baseada em Grafos)**
- **Trace visual**: Representa agentes como grafos de nós (estados) e arestas (transições).
  ```python
  from langgraph.graph import Graph
  graph = Graph().add_node("llm", llm_node).add_edge("llm", "tool").set_entry_point("llm")
  graph.invoke({"input": "Pergunta"})
  ```
- **Saída típica**:
  ```mermaid
  graph TD
    A[Entrada] --> B[LLM]
    B --> C[Ferramenta: Busca]
    C --> D[LLM]
    D --> E[Saída]
  ```
- **Vantagens**:
  - **Estrutura hierárquica**: Visualiza fluxos condicionais e loops.
  - **Depuração interativa**: Inspeção de estados intermediários via `graph.get_state()`.
  - **Logs detalhados**: Cada nó registra `checkpoint` (snapshot do estado).
    ```python
    state = graph.get_state(config={"configurable": {"thread_id": "1"}})
    print(state.values)  # {'llm_output': ..., 'tool_result': ...}
    ```

---
## **Comparação Direta**
| Critério               | LangChain (Tradicional)       | LangGraph (Grafo)              |
|------------------------|--------------------------------|--------------------------------|
| **Visualização**       | Logs textuais                  | Diagrama de fluxo (Mermaid)    |
| **Depuração de loops** | Manual (logs repetitivos)      | Automática (grafo cíclico)     |
| **Estado intermediário**| Limitado (logs brutos)         | Checkpoints completos          |
| **Complexidade**       | Ideal para cadeias lineares    | Melhor para workflows dinâmicos|
| **Ferramentas**        | `ConsoleCallbackHandler`       | `StateGraph`, `checkpointing`  |

---
## **Quando Usar Cada Um?**
- **LangChain**: Prototipação rápida ou agentes simples sem loops.
- **LangGraph**: Workflows complexos (ex: agentes com múltiplas ferramentas e condições).
```
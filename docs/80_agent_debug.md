```markdown
# Debug de Agents: Interpretando Traces Verbose

## Introdução
Ao desenvolver agentes com LangChain, traces verbose são essenciais para diagnosticar comportamentos inesperados. Este guia explica como interpretar logs detalhados gerados durante a execução de agentes.

---

## Configuração do Ambiente

```python
from langchain.agents import AgentExecutor
from langchain.callbacks import StdOutCallbackHandler
from langchain.globals import set_debug, set_verbose

# Habilita modo verbose global
set_debug(True)
set_verbose(True)

# Configura callback para logs detalhados
handler = StdOutCallbackHandler()
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    callbacks=[handler],
    verbose=True
)
```

---

## Estrutura de um Trace Verbose

Um trace típico contém:

1. **Input do Usuário**
   ```json
   {
     "input": "Quais são as previsões do tempo para São Paulo hoje?"
   }
   ```

2. **Interação do Agent**
   ```json
   {
     "action": "PesquisarPrevisãoDoTempo",
     "action_input": {"cidade": "São Paulo", "data": "2023-11-15"}
   }
   ```

3. **Observação do Ambiente**
   ```json
   {
     "observation": "Previsão: 25°C, ensolarado"
   }
   ```

4. **Decisão Final**
   ```json
   {
     "final_answer": "Hoje em São Paulo, a previsão é de 25°C e ensolarado."
   }
   ```

---

## Interpretando Erros Comuns

### 1. **Falta de Ferramentas**
```json
{
  "error": "ToolNotFound: Nenhuma ferramenta encontrada para 'PesquisarPrevisãoDoTempo'"
}
```
**Solução:** Verifique se a ferramenta está registrada no `AgentExecutor`.

### 2. **Timeout de Execução**
```json
{
  "error": "TimeoutError: Tempo limite excedido após 30s"
}
```
**Solução:** Ajuste `max_iterations` ou otimize o agente.

### 3. **Input Inválido**
```json
{
  "error": "ValidationError: 'cidade' é obrigatório"
}
```
**Solução:** Valide os parâmetros de entrada antes de chamar a ferramenta.

---

## Ferramentas de Debug

### 1. **Logs Personalizados**
```python
from langchain.callbacks import BaseCallbackHandler

class DebugHandler(BaseCallbackHandler):
    def on_agent_action(self, action, **kwargs):
        print(f"[DEBUG] Ação: {action.tool}")
        print(f"[DEBUG] Input: {action.tool_input}")

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    callbacks=[DebugHandler()]
)
```

### 2. **Visualização de Traces**
Use `LangSmith` para visualizar traces em um dashboard:
```python
from langchain.callbacks import LangChainTracer

tracer = LangChainTracer(project_name="debug-agent")
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    callbacks=[tracer]
)
```

---

## Boas Práticas

1. **Filtrar Logs Relevantes**
   Use `logging` para separar logs de debug de mensagens de usuário:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Testar Ferramentas Isoladamente**
   Verifique cada ferramenta antes de integrá-la ao agente.

3. **Limitar Iterações**
   Evite loops infinitos com `max_iterations`:
   ```python
   agent_executor = AgentExecutor(..., max_iterations=5)
   ```

4. **Validar Schemas de Input**
   Use Pydantic para validar inputs de ferramentas:
   ```python
   from pydantic import BaseModel

   class PrevisaoInput(BaseModel):
       cidade: str
       data: str
   ```

---
```
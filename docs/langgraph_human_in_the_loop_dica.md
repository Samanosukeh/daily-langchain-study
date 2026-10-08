```markdown
# **Human-in-the-loop: Pausar Grafo no LangChain**

## **1. Quando pausar o grafo?**
- **Validação de saída**: Verificar respostas críticas antes de prosseguir.
- **Decisões sensíveis**: Pausar em nós que exigem aprovação humana (ex.: pagamentos, dados sensíveis).
- **Debugging**: Inspecionar estados intermediários em fluxos complexos.

## **2. Implementação com `CallbackHandler`**
```python
from langchain.callbacks.base import BaseCallbackHandler

class HumanApprovalCallback(BaseCallbackHandler):
    def on_chain_end(self, outputs, **kwargs):
        if "approve" in outputs.get("next_actions", []):
            input("Pausar execução? Aperte Enter para continuar...")
```

## **3. Integrar ao grafo**
```python
from langchain.graphs import StateGraph

builder = StateGraph(...)
builder.add_node("human_approval", human_approval_node)
builder.add_conditional_edges("...", should_pause)
```

## **4. Ferramentas úteis**
- **`input()`**: Simples, mas bloqueia a execução.
- **FastAPI/Flask**: Para interfaces web (ex.: botão "Aprovar").
- **LangSmith**: Rastrear decisões humanas no histórico.

## **5. Boas práticas**
- **Timeout**: Limitar tempo de espera (`signal.alarm`).
- **Logs**: Registrar quem aprovou e quando.
- **Rollback**: Definir ações se a aprovação falhar.

## **6. Exemplo completo**
```python
def human_approval_node(state):
    print(f"Saída a validar: {state['output']}")
    input("Aprovar? (s/n): ").lower() == "s"
    return {"approved": True}
```
```
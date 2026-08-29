```markdown
# Callback Handlers Personalizados no LangChain

## Introdução
LangChain permite estender o comportamento padrão de callbacks com handlers personalizados. Isso é útil para integrar logs customizados, métricas ou interações com sistemas externos sem modificar o código da cadeia principal.

## Implementação Básica

```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Optional

class CustomCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any,
    ) -> None:
        print(f"LLM iniciou com prompt: {prompts[0][:50]}...")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        print(f"Cadeia finalizada. Output: {outputs}")
```

## Casos de Uso Comuns
1. **Logs estruturados**: Enviar eventos para um sistema de observabilidade (ex: Prometheus, Datadog).
2. **Interrupção condicional**: Parar execuções longas com base em heurísticas.
3. **Integração com APIs**: Notificar serviços externos sobre eventos (ex: Slack, Discord).

## Exemplo Avançado: Handler com Contexto

```python
class TrackingCallbackHandler(BaseCallbackHandler):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.events = []

    def on_tool_end(
        self,
        output: str,
        **kwargs: Any,
    ) -> None:
        self.events.append({
            "session_id": self.session_id,
            "event": "tool_end",
            "output": output
        })
```

## Boas Práticas
- **Evite lógica pesada** nos handlers (pode impactar performance).
- **Use `async`** para operações I/O (ex: chamadas HTTP).
- **Documente** os eventos suportados pelo handler.

## Referências
- [Documentação oficial de Callbacks](https://python.langchain.com/docs/modules/callbacks/)
- `BaseCallbackHandler` no código-fonte do LangChain.
```
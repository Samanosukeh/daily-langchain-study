```markdown
# Callbacks: Observabilidade nas Chains

## Introdução

Os **callbacks** no LangChain permitem interceptar e monitorar eventos durante a execução de uma `Chain`, `Agent` ou `Tool`. Eles são essenciais para **observabilidade**, **debugging**, **logging** e **integração com sistemas externos** (como APM, métricas ou telemetria).

---

## Conceitos Básicos

### O que são Callbacks?

- **Funções ou objetos** que são chamados em pontos específicos da execução de uma chain.
- Podem ser passados como parâmetro (`callbacks`) ou configurados globalmente (`callback_manager`).
- Suportam **assinaturas assíncronas** (`async`) para operações não-bloqueantes.

### Pontos de Chamada (Handler Types)

Os callbacks são acionados em **eventos específicos** durante a execução:

| Evento                     | Descrição                                                                 |
|----------------------------|---------------------------------------------------------------------------|
| `on_chain_start`           | Início da execução da chain.                                              |
| `on_chain_end`             | Término bem-sucedido da chain.                                            |
| `on_chain_error`           | Erro durante a execução da chain.                                         |
| `on_llm_start`             | Início da chamada ao LLM.                                                 |
| `on_llm_end`               | Término da chamada ao LLM.                                                |
| `on_llm_error`             | Erro durante a chamada ao LLM.                                            |
| `on_tool_start`            | Início da execução de uma ferramenta.                                     |
| `on_tool_end`              | Término da execução de uma ferramenta.                                    |
| `on_tool_error`            | Erro durante a execução de uma ferramenta.                                |
| `on_agent_action`          | Ação executada pelo agente (ex: uso de uma ferramenta).                   |
| `on_retriever_start`       | Início da recuperação de documentos (para chains com `Retriever`).         |
| `on_retriever_end`         | Término da recuperação de documentos.                                     |

---

## Implementação Básica

### 1. Callback Simples (Função)

```python
from langchain.callbacks.base import BaseCallbackHandler

class LoggingCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"🚀 LLM START: {prompts}")

    def on_llm_end(self, outputs, **kwargs):
        print(f"✅ LLM END: {outputs}")

    def on_chain_error(self, error, **kwargs):
        print(f"❌ CHAIN ERROR: {error}")

# Uso
from langchain.chains import LLMChain
from langchain.llms import OpenAI

llm = OpenAI()
chain = LLMChain(llm=llm, prompt="Diga olá para {name}")

chain.run(name="Alice", callbacks=[LoggingCallbackHandler()])
```

---

### 2. Callback Assíncrono (para APIs não-bloqueantes)

```python
import asyncio
from langchain.callbacks.base import BaseCallbackHandler

class AsyncLoggingCallbackHandler(BaseCallbackHandler):
    async def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"🚀 LLM START (Async): {prompts}")

    async def on_chain_end(self, outputs, **kwargs):
        print(f"✅ CHAIN END (Async): {outputs}")

# Uso com chain assíncrona
async def run_chain():
    llm = OpenAI()
    chain = LLMChain(llm=llm, prompt="Diga olá para {name}")
    await chain.arun(name="Bob", callbacks=[AsyncLoggingCallbackHandler()])

asyncio.run(run_chain())
```

---

### 3. Callback com Estado (Ex: Logging em Arquivo)

```python
from datetime import datetime
from langchain.callbacks.base import BaseCallbackHandler

class FileLoggingCallbackHandler(BaseCallbackHandler):
    def __init__(self, filename="chain_logs.txt"):
        self.filename = filename

    def _log(self, event: str, data: str):
        with open(self.filename, "a") as f:
            f.write(f"[{datetime.now()}] {event}: {data}\n")

    def on_chain_start(self, serialized, inputs, **kwargs):
        self._log("CHAIN_START", str(inputs))

    def on_chain_error(self, error, **kwargs):
        self._log("CHAIN_ERROR", str(error))
```

---
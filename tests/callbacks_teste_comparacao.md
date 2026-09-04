```markdown
# Comparação: Token Counters em LangChain

## Cenário
Teste de acumulação de tokens em cadeias (`chains`) com corrotinas (`coroutines`) em LangChain.

---

## 1. **LangChain com `AsyncTokenCounterCallback` (Padrão)**
```python
from langchain.callbacks import AsyncTokenCounterCallback
from langchain.chains import LLMChain

counter = AsyncTokenCounterCallback()
chain = LLMChain(llm=llm, callbacks=[counter])

await chain.arun("Texto para processamento")
print(f"Tokens consumidos: {counter.tokens_used}")
```

**Pros:**
- Integração nativa com callbacks do LangChain.
- Suporte assíncrono (`AsyncTokenCounterCallback`).
- Rastreamento automático de tokens de entrada/saída.

**Cons:**
- Overhead de inicialização do callback.
- Pode não capturar tokens em operações paralelas.

---

## 2. **TokenCounter com `tiktoken` + Middleware**
```python
import tiktoken
from langchain.schema import LLMResult

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

class TokenMiddleware:
    def __init__(self):
        self.total_tokens = 0

    def pre_run(self, prompt: str):
        self.total_tokens += count_tokens(prompt)

    def post_run(self, result: LLMResult):
        self.total_tokens += sum(count_tokens(msg) for msg in result.generations[0])

middleware = TokenMiddleware()
await chain.arun("Texto", callbacks=[middleware])
print(f"Total de tokens: {middleware.total_tokens}")
```

**Pros:**
- Controle fino sobre contagem (ex.: tokens de mensagens específicas).
- Independente de callbacks do LangChain.
- Baixo overhead.

**Cons:**
- Requer implementação manual de middleware.
- Não lida com tokens de contexto do modelo automaticamente.

---
## 3. **TokenCounter com `langchain-community` (Externo)**
```python
from langchain_community.callbacks import get_token_counter

counter = get_token_counter(model_name="gpt-3.5-turbo")
chain = LLMChain(llm=llm, callbacks=[counter])

await chain.arun("Texto")
print(f"Tokens usados: {counter.tokens}")
```

**Pros:**
- Solução pronta para uso (pacote `langchain-community`).
- Suporta múltiplos modelos.
- Fácil integração.

**Cons:**
- Dependência externa.
- Menos personalizável que implementações próprias.

---
### **Resumo Comparativo**
| Critério               | AsyncTokenCounter | Tiktoken + Middleware | langchain-community |
|------------------------|-------------------|-----------------------|---------------------|
| **Acurácia**           | Alta              | Alta                  | Alta                |
| **Desempenho**         | Médio             | Alto                  | Médio               |
| **Flexibilidade**      | Baixa             | Alta                  | Média               |
| **Dependência**        | LangChain         | tiktoken              | Pacote externo      |
| **Suporte Assíncrono** | Sim               | Sim                   | Sim                 |
```
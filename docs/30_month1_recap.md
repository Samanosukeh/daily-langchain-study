```markdown
# Resumo Mês 1: Do LLM Call à Chain LCEL

## 1. Introdução ao LCEL (LangChain Expression Language)
- **O que é LCEL?**
  - Linguagem declarativa para composição de chains no LangChain.
  - Permite encadeamento de componentes (LLMs, prompts, tools, etc.) de forma expressiva e eficiente.
  - Otimizado para produção (caching, streaming, fallback, etc.).

- **Benefícios**
  - Sintaxe simples e legível (`|` para encadeamento).
  - Suporte nativo a:
    - Streaming de tokens.
    - Tratamento de erros (`try-catch` com `fallback`).
    - Caching para reduzir custos.
    - Paralelismo com `RunnableParallel`.

---

## 2. Componentes Básicos do LCEL

### 2.1. `Runnable` (Interface Base)
- Todos os componentes no LCEL implementam a interface `Runnable`.
- Métodos principais:
  - `invoke()`: Execução síncrona.
  - `stream()`: Streaming de tokens/output.
  - `batch()`: Execução em lote.
  - `abatch()`: Batch assíncrono.
  - `astream()`: Streaming assíncrono.

Exemplo:
```python
from langchain_core.runnables import RunnableLambda

def dobro(x: int) -> int:
    return x * 2

runnable = RunnableLambda(dobro)
print(runnable.invoke(5))  # Saída: 10
```

---

### 2.2. Encadeamento com `|` (Pipe)
- Composição de `Runnables` usando o operador `|`.
- Exemplo básico:
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("Diga-me um {adjetivo} {substantivo}.")

chain = prompt | model
print(chain.invoke({"adjetivo": "bonito", "substantivo": "cachorro"}))
```

---

## 3. Prompts e LLMs no LCEL

### 3.1. Prompt Templates
- **`ChatPromptTemplate`**: Para modelos de chat (ex: GPT).
- **`PromptTemplate`**: Para modelos de texto puro.

Exemplo:
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente {role}."),
    ("user", "{input}")
])

chain = prompt | model
print(chain.invoke({"role": "técnico", "input": "Como usar o LCEL?"}))
```

### 3.2. Modelos (LLMs)
- **`ChatOpenAI`**, `ChatAnthropic`, etc.
- **Parâmetros**:
  - `model`: Nome do modelo.
  - `temperature`: Criatividade (0 a 1).
  - `max_tokens`: Limite de tokens.

---

## 4. Adicionando Output Parsers
- Converte saída do LLM em estruturas Python.
- Exemplo com `StrOutputParser`:
```python
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()
chain = prompt | model | output_parser
print(chain.invoke({"adjetivo": "rápido", "substantivo": "carro"}))
```

---

## 5. Encadeamento Avançado

### 5.1. `RunnableParallel` (Paralelismo)
- Executa múltiplas cadeias em paralelo.
```python
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel({
    "adjetivo": lambda x: x["adjetivo"].upper(),
    "substantivo": lambda x: x["substantivo"].lower()
}) | prompt | model | StrOutputParser()

print(chain.invoke({"adjetivo": "FELIZ", "substantivo": "GATO"}))
```

### 5.2. `RunnablePassthrough` (Passar Dados)
- Inclui dados adicionais sem modificação.
```python
from langchain_core.runnables import RunnablePassthrough

chain = {
    "adjetivo": lambda x: x["adjetivo"],
    "substantivo": RunnablePassthrough()
} | prompt | model | StrOutputParser()

print(chain.invoke({"adjetivo": "azul", "substantivo": "céu"}))
```

---

## 6. Tratamento de Er
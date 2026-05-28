```markdown
# Resumo LCEL: Runnables Disponíveis

## Visão Geral
LCEL (LangChain Expression Language) fornece uma interface unificada para compor e executar cadeias de componentes LangChain. O núcleo desta interface é o protocolo `Runnable`, que define métodos padrão para invocar, streaming, batching e paralelismo.

---

## Runnable Base

### `Runnable`
Interface base que todos os componentes LCEL implementam.

**Métodos principais:**
```python
class Runnable(Protocol):
    async def ainvoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output: ...
    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) | Output: ...
    async def abatch(self, inputs: List[Input], config: Optional[RunnableConfig] = None, *, return_exceptions: bool = False) -> List[Output]: ...
    def batch(self, inputs: List[Input], config: Optional[RunnableConfig] = None, *, return_exceptions: bool = False) -> List[Output]: ...
    async def astream(self, input: Input, config: Optional[RunnableConfig] = None) -> AsyncIterator[Output]: ...
    def stream(self, input: Input, config: Optional[RunnableConfig] = None) -> Iterator[Output]: ...
    def transform(self, input: Iterator[Input], config: Optional[RunnableConfig] = None) -> Iterator[Output]: ...
```

---

## Runnables Implementados

### 1. `RunnableLambda`
Executa funções Python arbitrariamente.

```python
from langchain_core.runnables import RunnableLambda

def func(input: str) -> str:
    return input.upper()

runnable = RunnableLambda(func)
result = runnable.invoke("hello")  # "HELLO"
```

---

### 2. `RunnableParallel`
Executa múltiplos Runnables em paralelo.

```python
from langchain_core.runnables import RunnableParallel

runnable = RunnableParallel(
    a=RunnableLambda(lambda x: x + 1),
    b=RunnableLambda(lambda x: x * 2)
)
result = runnable.invoke(1)  # {"a": 2, "b": 2}
```

---

### 3. `RunnablePassthrough`
Passa a entrada adiante sem modificação.

```python
from langchain_core.runnables import RunnablePassthrough

runnable = RunnablePassthrough()
result = runnable.invoke("data")  # "data"
```

---

### 4. `RunnableAssign`
Adiciona/atualiza chaves em um dicionário de entrada.

```python
from langchain_core.runnables import RunnableAssign

runnable = RunnableAssign({"nova_chave": lambda x: x["original"] * 2})
result = runnable.invoke({"original": 5})  # {"original": 5, "nova_chave": 10}
```

---

### 5. `RunnableBranch`
Aplica lógica condicional com múltiplos Runnables.

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x < 0, RunnableLambda(lambda x: "negativo")),
    (lambda x: x == 0, RunnableLambda(lambda x: "zero")),
    RunnableLambda(lambda x: "positivo")
)
result = branch.invoke(-1)  # "negativo"
```

---

### 6. `RunnableMap`
Aplica um Runnable a cada item de um dicionário.

```python
from langchain_core.runnables import RunnableMap

runnable = RunnableMap({
    "dobro": RunnableLambda(lambda x: x * 2),
    "quadrado": RunnableLambda(lambda x: x ** 2)
})
result = runnable.invoke(3)  # {"dobro": 6, "quadrado": 9}
```

---

### 7. `RunnableSequence`
Encadeia múltiplos Runnables em sequência.

```python
from langchain_core.runnables import RunnableSequence

seq = RunnableSequence(
    first=RunnableLambda(lambda x: x + 1),
    last=RunnableLambda(lambda x: x * 2)
)
result = seq.invoke(1)  # 4
```

---

## Configuração Avançada

### `RunnableConfig`
Controla comportamento de execução.

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    tags=["minha_tag"],
    metadata={"chave": "valor"},
    recursion_limit=50
)
```

---

## Métodos Úteis

### `.pipe()`
Encadeia Runnables de forma fluida.

```python
chain = (
    RunnableLambda(lambda x: x + 1)
    | RunnableLambda(lambda x: x
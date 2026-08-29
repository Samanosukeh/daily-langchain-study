```markdown
# Callback Customizado: Logar Tokens em LangChain

## 1. Estrutura Básica
Crie uma classe herdando de `BaseCallbackHandler` e implemente métodos como `on_llm_start`, `on_llm_end`, etc.

```python
from langchain.callbacks.base import BaseCallbackHandler

class TokenLoggerHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"Tokens de entrada: {prompts}")

    def on_llm_end(self, outputs, **kwargs):
        print(f"Tokens de saída: {outputs}")
```

## 2. Integração com Chain
Passe o handler para o `LLMChain` ou `Agent`:

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain

llm = OpenAI()
handler = TokenLoggerHandler()
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
```

## 3. Logar para Arquivo
Adicione logging com `logging` ou `print` para persistência:

```python
import logging

logging.basicConfig(filename='tokens.log', level=logging.INFO)

class TokenLoggerHandler(BaseCallbackHandler):
    def on_llm_end(self, outputs, **kwargs):
        logging.info(f"Tokens gerados: {outputs}")
```

## 4. Métricas de Uso
Conte tokens com `tiktoken` para análise:

```python
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

class TokenCounterHandler(BaseCallbackHandler):
    def on_llm_end(self, outputs, **kwargs):
        tokens = len(encoding.encode(outputs["generations"][0][0]["text"]))
        print(f"Tokens totais: {tokens}")
```

## 5. Debugging
Use `verbose=True` para logs detalhados:

```python
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler], verbose=True)
```

## 6. Múltiplos Handlers
Combine handlers para diferentes propósitos:

```python
from langchain.callbacks.stdout import StdOutCallbackHandler

handlers = [TokenLoggerHandler(), StdOutCallbackHandler()]
chain = LLMChain(llm=llm, prompt=prompt, callbacks=handlers)
```

## 7. Desempenho
Evite processamento pesado nos callbacks para não impactar a execução.
```
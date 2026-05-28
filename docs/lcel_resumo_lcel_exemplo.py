```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Dados de entrada
documentos = [
    {"id": 1, "texto": "LangChain é uma framework para aplicações LLM."},
    {"id": 2, "texto": "LCEL é a linguagem de composição do LangChain."},
]

# Pipeline LCEL minimalista
cadeia = (
    {"texto": RunnablePassthrough()}  # Passa texto diretamente
    | StrOutputParser()  # Converte para string
)

# Execução
for doc in documentos:
    resultado = cadeia.invoke(doc["texto"])
    print(f"ID {doc['id']}: {resultado}")
```
```markdown
# Comparação: Filtros de Metadata em LangChain

## Cenário
Testar diferentes abordagens para filtrar resultados com base em metadata em cadeias (`chains`) do LangChain.

---

## 1. **Filtro Manual (Python puro)**
```python
from langchain.schema import Document

docs = [
    Document(page_content="Texto 1", metadata={"score": 0.9, "source": "A"}),
    Document(page_content="Texto 2", metadata={"score": 0.4, "source": "B"}),
]

# Filtro manual
filtered = [doc for doc in docs if doc.metadata.get("score", 0) > 0.5]
```
**Vantagens**:
- Controle total sobre a lógica.
**Desvantagens**:
- Código verboso para casos complexos.

---

## 2. **Filtro com `metadata` no Retriever**
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import DocumentCompressorPipeline

# Usando `filter` no retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"filter": {"score": {"$gte": 0.5}}}
)
```
**Vantagens**:
- Integrado ao banco de dados vetorial (ex: Chroma, Pinecone).
**Desvantagens**:
- Sintaxe específica do banco (ex: MongoDB).

---

## 3. **Filtro com `MetadataFilter` (LangChain v0.1+)**
```python
from langchain_core.filters import MetadataFilter

filter = MetadataFilter(
    key="source",
    value="A",
    operator="=="
)

# Aplicado em cadeias
chain = (
    {"context": retriever | filter}
    | prompt
    | llm
)
```
**Vantagens**:
- Sintaxe unificada para diferentes bancos.
**Desvantagens**:
- Requer LangChain >= 0.1.0.

---
## 4. **Filtro com `RunnableLambda` (Customização)**
```python
from langchain_core.runnables import RunnableLambda

def filter_docs(docs):
    return [doc for doc in docs if doc.metadata.get("source") == "A"]

chain = (
    retriever
    | RunnableLambda(filter_docs)
    | prompt
    | llm
)
```
**Vantagens**:
- Flexível para lógicas complexas.
**Desvantagens**:
- Performance pode ser impactada em grandes volumes.

---
## **Resumo Comparativo**
| Abordagem          | Controle | Integração | Performance | Complexidade |
|--------------------|----------|------------|-------------|--------------|
| Manual             | Alta     | Baixa      | Alta        | Média        |
| Retriever Filter   | Média    | Alta       | Alta        | Baixa        |
| MetadataFilter     | Média    | Alta       | Média       | Baixa        |
| RunnableLambda     | Alta     | Média      | Baixa       | Alta         |
```
```markdown
# **Nota Técnica: Testes de Filtragem em LangChain com `filter`**

## **Contexto**
Ao testar pipelines de LangChain que utilizam filtros dinâmicos (ex.: `filter` em `RetrievalQA`), é comum encontrar inconsistências entre os resultados esperados e os retornados. Este documento aborda um aspecto secundário: **validação de filtros em tempo de execução** usando `RunnableParallel` e `RunnablePassthrough`.

---

## **Problema Identificado**
Filtros como `filter: { "metadata.type": "document" }` podem falhar em dois cenários:
1. **Chaves ausentes**: Se `metadata` não existir no documento, o filtro ignora o registro (comportamento padrão do MongoDB-style filter).
2. **Tipos incompatíveis**: Comparações como `filter: { "score": { "$gt": 0.5 } }` falham se `score` for `None` ou string.

---

## **Solução Proposta**
### **1. Pré-processamento com `RunnablePassthrough.assign`**
Adiciona chaves ausentes ou normaliza tipos antes da filtragem:

```python
from langchain_core.runnables import RunnablePassthrough

def normalize_metadata(doc):
    return {
        **doc,
        "metadata": {
            **doc.get("metadata", {}),
            "type": doc.get("metadata", {}).get("type", "unknown")
        },
        "score": float(doc.get("score", 0.0))
    }

preprocess_chain = RunnablePassthrough.assign(
    doc=normalize_metadata
)
```

### **2. Filtro Dinâmico com `RunnableParallel`**
Combina pré-processamento e filtragem em um único passo:

```python
from langchain_core.runnables import RunnableParallel

filter_chain = RunnableParallel({
    "filtered_docs": (
        preprocess_chain
        | {"docs": lambda x: [x["doc"]]}
        | retriever  # Assume que `retriever` usa o filtro
    )
})
```

---

## **Validação**
Teste com um documento incompleto:
```python
test_doc = {"content": "Teste", "metadata": {"author": "user"}}  # Sem "type" ou "score"
result = await filter_chain.ainvoke(test_doc)
print(result["filtered_docs"])  # Deve retornar o documento normalizado
```

---

## **Considerações**
- **Performance**: O `RunnablePassthrough.assign` adiciona overhead. Use apenas em filtros complexos.
- **Erros silenciosos**: Sempre valide a estrutura dos documentos antes de aplicar filtros.
- **Alternativa**: Para filtros avançados, considere usar `pydantic.BaseModel` para validação de entrada.

---
**Referências**:
- [LangChain Docs: Filters](https://python.langchain.com/docs/modules/data_connection/retrievers/)
- [MongoDB Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query/)
```
```markdown
# Notas Técnicas: MMR Retriever - Filtro de Similaridade Mínima

## Objetivo
Implementar um filtro adicional no `MMRRetriever` para evitar documentos com similaridade abaixo de um limite configurável.

## Implementação

```python
from typing import List, Optional
from langchain.retrievers import MMRRetriever
from langchain.schema import Document
import numpy as np

class ThresholdMMRRetriever(MMRRetriever):
    def __init__(
        self,
        embeddings,
        documents: List[Document],
        weights: List[float],
        lambda_mult: float = 0.5,
        threshold: float = 0.1,
    ):
        super().__init__(
            embeddings=embeddings,
            documents=documents,
            weights=weights,
            lambda_mult=lambda_mult,
        )
        self.threshold = threshold

    def _mmr_retrieve(
        self,
        query_embedding: np.ndarray,
        k: int = 4,
        fetch_k: int = 20,
    ) -> List[Document]:
        """Override com filtro de similaridade mínima."""
        docs_and_scores = self.vectorstore.similarity_search_by_vector(
            query_embedding,
            k=fetch_k,
        )

        # Filtra documentos abaixo do threshold
        filtered = [
            (doc, score)
            for doc, score in docs_and_scores
            if score >= self.threshold
        ]

        if not filtered:
            return []

        # Aplica MMR nos documentos filtrados
        return self._mmr_select(
            query_embedding=query_embedding,
            docs_and_scores=filtered,
            k=k,
        )
```

## Configuração
```python
retriever = ThresholdMMRRetriever(
    embeddings=embeddings,
    documents=documents,
    weights=[0.5, 0.3, 0.2],
    threshold=0.15,  # Similaridade mínima aceitável
)
```

## Considerações
- **Impacto no desempenho**: O filtro reduz o espaço de busca antes da aplicação do MMR.
- **Ajuste do threshold**: Valores muito altos podem retornar menos documentos que o esperado.
- **Compatibilidade**: Mantém a interface original do `MMRRetriever`.

## Exemplo de Uso
```python
query = "documentos relevantes sobre IA"
docs = retriever.get_relevant_documents(query)
print(f"Retornados {len(docs)} documentos")
```

## Referências
- LangChain MMRRetriever: [Documentação Oficial](https://python.langchain.com/docs/modules/data_connection/retrievers/mmrmulti_vector)
```
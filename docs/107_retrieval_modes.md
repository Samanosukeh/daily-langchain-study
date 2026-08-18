```markdown
# Similarity vs MMR: quando usar cada um

## Introdução

Ao implementar um sistema de **RAG (Retrieval-Augmented Generation)**, a escolha do método de recuperação de documentos é crucial para a qualidade das respostas geradas. Dois métodos comuns são:

1. **Similarity Search (Busca por Similaridade)**
2. **Maximal Marginal Relevance (MMR)**

Este documento explica quando e como usar cada um, com exemplos práticos em Python usando LangChain.

---

## 1. Similarity Search (Busca por Similaridade)

### O que é?
A **Similarity Search** recupera documentos com base na similaridade semântica com a consulta do usuário. Utiliza embeddings (vetores densos) para calcular a distância (ex: cosseno) entre a consulta e os documentos.

### Quando usar?
- **Consultas diretas e factuais**: Quando a resposta exige documentos altamente relevantes e próximos semanticamente à consulta.
- **Precisão é prioridade**: Quando você quer evitar documentos que, embora semanticamente próximos, não sejam diretamente úteis.
- **Domínios técnicos ou específicos**: Em áreas onde a relevância direta é mais importante do que a diversidade.

### Exemplo em LangChain

```python
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Carregar embeddings e documentos
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("meu_banco_de_dados", embeddings, allow_dangerous_deserialization=True)

# Similarity Search
query = "Quais são os sintomas da diabetes?"
docs = db.similarity_search(query, k=3)  # k = número de documentos retornados
for doc in docs:
    print(doc.page_content)
    print("---")
```

### Vantagens
- **Simplicidade**: Fácil de implementar e entender.
- **Alta precisão**: Retorna documentos muito próximos à consulta.

### Desvantagens
- **Falta de diversidade**: Pode retornar documentos muito semelhantes entre si, perdendo contexto variado.
- **Ruído em consultas ambíguas**: Pode recuperar documentos irrelevantes se a consulta for vaga.

---

## 2. Maximal Marginal Relevance (MMR)

### O que é?
O **MMR** é um método que busca um equilíbrio entre **relevância** e **diversidade**. Ele maximiza a relevância dos documentos em relação à consulta, mas minimiza a similaridade entre os próprios documentos recuperados.

### Fórmula
```
MMR = argmax [ λ * Similaridade(consulta, doc_i) - (1-λ) * max(Similaridade(doc_i, doc_j)) ]
```
- `λ` (lambda): Parâmetro entre 0 e 1 que controla o trade-off entre relevância e diversidade.
  - **λ próximo a 1**: Prioriza relevância.
  - **λ próximo a 0**: Prioriza diversidade.

### Quando usar?
- **Consultas complexas ou abertas**: Quando a resposta precisa de múltiplos ângulos ou perspectivas.
- **Evitar redundância**: Quando você quer evitar que documentos muito semelhantes sejam recuperados.
- **Exploração de tópicos**: Em cenários onde a diversidade de informações é mais importante do que a precisão absoluta.

### Exemplo em LangChain

```python
# MMR Search
docs_mmr = db.max_marginal_relevance_search(query, k=3, lambda_mult=0.7)
for doc in docs_mmr:
    print(doc.page_content)
    print("---")
```

### Vantagens
- **Diversidade**: Retorna documentos com perspectivas diferentes.
- **Equilíbrio**: Controla o trade-off entre relevância e diversidade via `lambda`.

### Desvantagens
- **Complexidade**: Requer ajuste fino do parâmetro `lambda`.
- **Menor precisão em consultas específicas**: Pode recuperar documentos menos diretamente relevantes.

---

## Comparação Direta

| Critério               | Similarity Search       | MMR                      |
|------------------------|-------------------------|--------------------------|
| **Foco principal**     | Relevância direta       | Relevância + diversidade |
| **Parâmetros**         | `k` (número de docs)    | `k`, `lambda`            |
| **Complexidade**       | Baixa                   | Média                    |
| **Uso recomendado**    | Consultas factuais      | Consultas complexas      |
| **Redundância**        | Alta                    | Baixa                    |
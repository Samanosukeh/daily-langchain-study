```markdown
# Similarity vs MMR: Quando Usar Cada Um

## **Similarity Search (Busca por Similaridade)**
- **Use quando**: Precisa recuperar os documentos *mais relevantes* para uma consulta.
- **Como funciona**: Ordena documentos pela similaridade com a query (ex: cosine similarity).
- **Exemplo**:
  ```python
  docs = vectorstore.similarity_search(query, k=3)
  ```
- **Vantagem**: Simples e eficiente para recuperar os *top-k* mais similares.
- **Desvantagem**: Pode retornar documentos redundantes ou pouco diversificados.

---

## **Maximal Marginal Relevance (MMR)**
- **Use quando**: Precisa de *diversidade* nos resultados (evita redundância).
- **Como funciona**: Balanceia relevância e dissimilaridade entre documentos.
- **Exemplo**:
  ```python
  docs = vectorstore.max_marginal_relevance_search(query, k=3, lambda_mult=0.5)
  ```
- **Vantagem**: Resultados mais variados e abrangentes.
- **Desvantagem**: Menos focado em relevância pura.

---

## **Quando Escolher Cada Um?**
| **Caso de Uso**               | **Similarity** | **MMR**          |
|-------------------------------|---------------|------------------|
| Respostas diretas e precisas  | ✅ Sim         | ❌ Não           |
| Sumarização ou overview       | ❌ Não         | ✅ Sim           |
| Evitar duplicidade            | ❌ Não         | ✅ Sim           |
| Busca em base de conhecimento | ✅ Sim         | ⚠️ Depende       |

---

## **Dica Extra**
- **Combine ambos**: Use `similarity_search` para relevância inicial e `MMR` para pós-processamento.
```
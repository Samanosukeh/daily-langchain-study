```markdown
# Similarity vs MMR: Quando Usar Cada Abordagem em Recuperação de Documentos

## **Similarity Search (Busca por Similaridade)**
- **Foco**: Retorna documentos mais similares à consulta, priorizando relevância direta.
- **Métrica**: Usa embeddings e distância vetorial (ex: cosseno, euclidiana).
- **Vantagens**:
  - Simples e intuitivo.
  - Excelente para consultas diretas onde a similaridade exata é crítica.
- **Desvantagens**:
  - Pode retornar documentos redundantes (ex: várias versões de um mesmo conteúdo).
  - Não considera diversidade entre os resultados.
- **Casos de uso**:
  - Buscas em bases de conhecimento fechadas.
  - Sistemas de recomendação baseados em conteúdo.
- **Exemplo em LangChain**:
  ```python
  from langchain.vectorstores import FAISS
  db = FAISS.from_documents(docs, embeddings)
  docs = db.similarity_search("consulta", k=3)
  ```

---

## **Maximal Marginal Relevance (MMR)**
- **Foco**: Balanceia relevância e diversidade, evitando redundância.
- **Métrica**: Combina similaridade com "marginal relevance" (novidade em relação aos já selecionados).
- **Vantagens**:
  - Evita repetição de resultados.
  - Ideal para buscas que precisam cobrir múltiplos aspectos de uma consulta.
- **Desvantagens**:
  - Mais complexo de configurar (parâmetro `lambda_mult` para balanceamento).
  - Pode sacrificar relevância em prol de diversidade.
- **Casos de uso**:
  - Buscas em bases grandes/diversas (ex: web, artigos científicos).
  - Sistemas de Q&A com necessidade de múltiplas perspectivas.
- **Exemplo em LangChain**:
  ```python
  docs = db.max_marginal_relevance_search("consulta", k=3, lambda_mult=0.5)
  ```

---
## **Comparação Direta**
| Critério          | Similarity Search       | MMR                     |
|-------------------|-------------------------|-------------------------|
| **Diversidade**   | Baixa (risco de repetição) | Alta (evita redundância) |
| **Complexidade**  | Baixa                   | Média (ajuste de `lambda_mult`) |
| **Performance**   | Rápida                  | Lenta (cálculo adicional) |
| **Cenário Ideal** | Consultas diretas       | Buscas exploratórias    |

---
## **Quando Usar Cada Um?**
- **Use Similarity Search** quando:
  - A consulta é simples e requer respostas diretas.
  - A base de dados é pequena ou homogênea.
  - Prioridade é a relevância pura.

- **Use MMR** quando:
  - A consulta é ambígua ou requer múltiplas perspectivas.
  - A base de dados é grande e diversificada.
  - Você precisa evitar resultados repetidos ou similares demais.

---
## **Combinação Híbrida**
- **Sugestão**: Use MMR para os primeiros `k` resultados e, em seguida, filtre por similaridade para priorizar os mais relevantes dentre os diversos.
```python
mixed_docs = db.max_marginal_relevance_search("consulta", k=5)
final_docs = sorted(mixed_docs, key=lambda x: x.similarity_score, reverse=True)[:3]
```
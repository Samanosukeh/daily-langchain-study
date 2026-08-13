```markdown
## Reflexão sobre o teste: retriever retorna k documentos

O teste de um retriever que retorna `k` documentos é fundamental para validar a eficácia do mecanismo de recuperação em sistemas de busca ou RAG. O foco deve estar na **qualidade dos documentos recuperados**, não apenas na quantidade.

### Pontos críticos a validar:
1. **Relevância dos documentos**: Os top `k` resultados devem conter informações diretamente relacionadas à consulta. Um teste automatizado com métricas como `MRR` (Mean Reciprocal Rank) ou `Hit Rate@k` ajuda a quantificar isso.
2. **Diversidade**: O retriever não deve retornar documentos redundantes. Um teste com `k=5` deve garantir que os resultados cubram diferentes aspectos da query.
3. **Ordenação**: A ordem dos documentos importa. Um teste de `ranking` pode verificar se os documentos mais relevantes estão nas primeiras posições.
4. **Limites de `k`**: Testar diferentes valores de `k` (ex: 3, 5, 10) para avaliar como o retriever se comporta com diferentes profundidades de busca.

### Implementação prática:
```python
def test_retriever_returns_k_docs(retriever, query, k=5):
    docs = retriever.invoke(query)
    assert len(docs) == k, f"Esperado {k} documentos, mas retornou {len(docs)}"
    assert all(doc.metadata.get("relevance") > 0 for doc in docs), "Documentos irrelevantes retornados"
```
**Observação**: Em sistemas de produção, é comum usar `k` maior (ex: 20) e aplicar filtros adicionais (ex: reranking) para melhorar a qualidade final.
```
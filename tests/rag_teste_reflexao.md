```markdown
## Reflexão: Teste de busca com FAISS

Ao testar a busca de documentos com FAISS, percebi que a eficácia depende diretamente de dois fatores:

1. **Qualidade da embeddings**: Documentos mal representados vetorialmente (embeddings ruins) levam a resultados imprecisos, mesmo com um índice otimizado. A normalização dos vetores (`normalize=True` na criação do índice) ajudou a reduzir vieses de magnitude.

2. **Parâmetros de busca**:
   - `k` (número de vizinhos): Valores muito altos ou baixos degradam a relevância. Testei `k=5` para um equilíbrio entre performance e precisão.
   - Métrica de distância: `L2` funcionou melhor que `IP` (Inner Product) em meus testes com embeddings de texto curto, provavelmente por ser menos sensível a outliers.

**Problema encontrado**:
A busca retornava documentos semanticamente distantes quando a consulta era ambígua (ex.: "Python" como linguagem vs. animal). Solução parcial: usar *query expansion* com sinônimos antes da busca.

**Conclusão**:
FAISS é rápido e escalável, mas exige:
- Embeddings de qualidade (ex.: `sentence-transformers/all-MiniLM-L6-v2`).
- Ajuste fino de parâmetros (`efConstruction`, `efSearch` para HNSW).
- Pós-processamento dos resultados (re-ranking com BM25 ou filtros semânticos).

Próximo passo: integrar reranking com Cross-Encoder para validar se a precisão melhora em cenas de ambiguidade.
```
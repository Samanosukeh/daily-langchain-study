```markdown
# Reflexão sobre Comentários em Loaders e Vector Stores no LangChain

Ao trabalhar com `loaders` e `vector stores` no LangChain, os comentários são essenciais para documentar intenções, limitações e fluxos não óbvios. No entanto, há um equilíbrio delicado:

1. **Clareza vs. Ruído**: Comentários óbvios (ex: `# Carrega o arquivo`) não agregam valor. Priorize explicar *por que* um loader específico foi escolhido (ex: `# Usa TextLoader para evitar quebra de linhas em arquivos .txt`).

2. **Contextualização de Parâmetros**: Em `vector stores`, comentários como `# `eficiencia=0.7` para filtros de similaridade` ajudam a lembrar trade-offs entre precisão e performance.

3. **Códigos Legados**: Em projetos com múltiplos `loaders`, um comentário como `# Loader herdado da migração v1.2 — substituir por UnstructuredFileLoader em 2024` evita dívidas técnicas.

4. **Debugging**: Comentários como `# `embeddings=OpenAIEmbeddings(model="text-embedding-3-small")` — custo: ~$0.02/1k tokens` facilitam auditorias de custo e performance.

5. **Performance**: Em loaders de grandes volumes, um comentário como `# Batch size=1000 para evitar OOM no processamento` documenta decisões críticas.

**Regra prática**: Se um trecho de código não for trivial em 3 meses, comente-o. Caso contrário, deixe o código falar por si.
```
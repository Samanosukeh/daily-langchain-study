```markdown
# RetrievalQA Chain: Pergunta + Contexto Dinâmico

A `RetrievalQA` chain do LangChain é uma abordagem poderosa para integrar recuperação de documentos com modelos de linguagem, permitindo respostas baseadas em contexto externo sem retreinamento do LLM. O fluxo básico é simples: uma pergunta é recebida, um mecanismo de busca (retriever) extrai trechos relevantes de uma base de documentos, e o LLM processa esses trechos para gerar uma resposta.

O ponto crítico aqui é a **qualidade do retriever**. Um índice vetorial mal configurado (e.g., embeddings ruins ou threshold de similaridade inadequado) pode retornar trechos irrelevantes, degradando a resposta final. Testes com diferentes métodos de chunking (e.g., `RecursiveCharacterTextSplitter` vs. `TokenTextSplitter`) e métricas de similaridade (cosine, dot product) são essenciais.

Outro desafio é o **contexto limitado**. Mesmo com um retriever eficiente, o LLM tem uma janela de contexto fixa (ex: 4K tokens). Se os documentos recuperados forem longos, a cadeia pode truncar informações importantes. Soluções incluem:
- Usar `load_max_tokens` no retriever para limitar o tamanho dos chunks.
- Implementar *reranking* com modelos leves (e.g., `CrossEncoder`) para priorizar trechos mais relevantes.

Por fim, a **interatividade** é limitada. A `RetrievalQA` padrão não permite feedback em tempo real ou refinamento iterativo da busca. Para casos avançados, é necessário estender a cadeia com loops de auto-correção ou integração com RAG adaptativo.

*Conclusão*: A `RetrievalQA` é uma ferramenta valiosa, mas seu sucesso depende de ajustes finos no pipeline de recuperação e no gerenciamento de contexto.
```
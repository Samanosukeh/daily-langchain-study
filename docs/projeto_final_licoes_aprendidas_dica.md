```markdown
# Lições aprendidas: 6 meses de LangChain

## 1. **Comece com os conceitos básicos**
- Domine `PromptTemplate`, `LLMChain` e `RetrievalQA` antes de avançar.
- Evite pular para `Agents` ou `Tools` sem entender o fluxo básico.

## 2. **Gerenciamento de memória é crucial**
- Use `ConversationBufferMemory` para diálogos simples.
- Para casos complexos, experimente `ConversationSummaryMemory` ou `VectorStoreRetrieverMemory`.

## 3. **Embeddings e vetorização são seus aliados**
- `HuggingFaceEmbeddings` ou `OpenAIEmbeddings` + `FAISS`/`Chroma` para RAG eficiente.
- Normalize embeddings para melhorar a similaridade.

## 4. **Debugging é inevitável**
- Ative logs com `logging.basicConfig(level=logging.INFO)`.
- Use `print()` ou `pdb` para inspecionar objetos intermediários.

## 5. **Nem tudo precisa de LangChain**
- Para pipelines simples, `LLMChain` pode ser overkill.
- Considere chamadas diretas à API se a complexidade for baixa.

## 6. **Cuidado com a latência**
- Cache respostas com `Redis` ou `SQLite` para evitar chamadas repetidas.
- Otimize prompts para reduzir tokens e tempo de resposta.

## 7. **Integração com APIs externas**
- Use `Requests` ou `httpx` para APIs não suportadas nativamente.
- Valide respostas antes de passá-las para o LLM.

## 8. **Versionamento de prompts**
- Armazene prompts em arquivos `.txt` ou `.json` para reutilização.
- Documente mudanças com `git` para rastrear evoluções.

## 9. **Segurança em primeiro lugar**
- Sanitize inputs/outputs para evitar injeção de prompts.
- Nunca exponha chaves de API em código público.

## 10. **Documentação é sua salvação**
- Documente cada componente customizado com docstrings.
- Mantenha um `README.md` com exemplos de uso.

## 11. **Performance vs. Custo**
- Ajuste `temperature` e `top_p` para balancear criatividade e precisão.
- Monitore custos de tokens em APIs pagas.

## 12. **Testes automatizados**
- Use `pytest` para validar cadeias (`chains`) e prompts.
- Teste casos edge-case (ex.: inputs vazios).

## 13. **Comunidade é poderosa**
- Siga issues no [GitHub LangChain](https://github.com/langchain-ai/langchain).
- Participe de discussões no [Discord LangChain](https://discord.gg/langchain).

## 14. **Mantenha-se atualizado**
- LangChain evolui rápido: acompanhe releases e breaking changes.
- Subscreva newsletters como [LangChain Newsletter](https://blog.langchain.dev/).

## 15. **Pratique, pratique, pratique**
- Clone repositórios como [LangChain Examples](https://github.com/langchain-ai/langchain/tree/master/examples).
- Modifique exemplos para casos de uso reais.
```
```markdown
# Dicas Rápidas sobre LCEL (LangChain Expression Language)

## O que é LCEL?
- **Linguagem declarativa** para composição de pipelines no LangChain.
- **Baseado em expressões** do Python (similar a `lambda` ou list comprehensions).
- **Otimizado para LangChain**, mas pode ser usado fora dele.

## Principais Características
- **Encadeamento de componentes**: Combine `LLMs`, `Retrievers`, `Tools`, etc., de forma fluida.
- **Suporte a async/await**: Execute operações de forma não-bloqueante.
- **Avaliação preguiçosa (lazy)**: Processamento sob demanda, ideal para streams.

## Sintaxe Básica
```python
# Pipeline simples com LCEL
prompt = PromptTemplate.from_template("Diga-me um fato sobre {topic}")
llm = ChatOpenAI(temperature=0)
chain = prompt | llm  # Encadeamento com pipe (|)
response = chain.invoke({"topic": "Python"})
```

## Operadores Úteis
- `|` (pipe): Encadeia componentes sequencialmente.
- `RunnablePassthrough`: Passa dados adiante sem modificação.
- `RunnableParallel`: Executa múltiplas branches em paralelo.

## Boas Práticas
- Use `bind()` para passar parâmetros adicionais (ex: `temperature`).
- Prefira `invoke()` para execução síncrona e `astream()` para streams.
- Debug com `print()` ou `inspect` em cada etapa do pipeline.

## Exemplo com Retrieval
```python
retriever = vectorstore.as_retriever()
template = """Responda usando apenas o contexto abaixo:
Contexto: {context}
Pergunta: {question}"""
prompt = PromptTemplate.from_template(template)
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
```

## Debugging
- Ative logs com `export LANGCHAIN_VERBOSE=true`.
- Use `RunnableLambda` para funções personalizadas.
- Inspecione cada etapa com `chain.get_graph()` (visualização do pipeline).

## Performance
- LCEL é **otimizado para LangChain**, mas pode ser lento com LLMs externos.
- Cache respostas com `cache=True` em `ChatOpenAI`.
- Use `async` para I/O-bound operações (ex: chamadas a APIs).

## Recursos
- [Documentação Oficial](https://python.langchain.com/docs/expression_language/)
- [Exemplos no GitHub](https://github.com/langchain-ai/langchain/tree/master/libs/langchain/langchain/experimental)
```
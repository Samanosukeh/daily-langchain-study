```markdown
# Notas Técnicas: LangChain - *RetrievalQA* com Memória de Sessão

## Introdução
O `RetrievalQA` é um padrão comum em LangChain para criar sistemas de Q&A que combinam **recuperação de documentos** (RAG) com **modelos de linguagem**. Contudo, sua integração com **memória de sessão** (ex.: `ConversationBufferMemory`) é menos documentada, mas viável para manter contexto em interações longas.

---

## Implementação Básica com Memória

```python
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Carregar embeddings e vetorizar documentos
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(["Texto 1", "Texto 2"], embeddings)

# Inicializar memória
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Configurar RetrievalQA com memória
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,  # Modelo de linguagem (ex.: ChatOpenAI)
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    memory=memory,
    verbose=True
)

# Executar pergunta com contexto
resposta = qa_chain.run("Qual é a capital do Brasil?")
print(resposta)  # Resposta inicial

# Pergunta de acompanhamento (usa histórico)
resposta = qa_chain.run("E qual a população dela?")
```

---

## Pontos Críticos

1. **Contexto Limitado**:
   - `ConversationBufferMemory` armazena **todas as mensagens**, mas o `RetrievalQA` só injeta `chat_history` no prompt se o `chain_type` for `"refine"` ou `"map_reduce"` (não `"stuff"`).
   - Solução: Usar `ConversationalRetrievalChain` (mais adequado para RAG + memória).

2. **Formato do Histórico**:
   - O histórico deve ser uma lista de dicionários com chaves `input` e `output`:
     ```python
     memory.chat_memory.add_user_message("Pergunta 1")
     memory.chat_memory.add_ai_message("Resposta 1")
     ```

3. **Overhead de Tokens**:
   - Histórico longo aumenta o uso de tokens. Considere:
     - `ConversationSummaryMemory` para resumir contexto.
     - `ConversationBufferWindowMemory` para limitar mensagens antigas.

---
## Alternativa Recomendada

Para RAG + memória, prefira:
```python
from langchain.chains import ConversationalRetrievalChain

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory
)
```

**Vantagem**: Gerencia automaticamente a injeção de contexto e recuperação de documentos em loop.
```
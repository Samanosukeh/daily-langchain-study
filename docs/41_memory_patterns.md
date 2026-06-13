```markdown
# Resumo: Padrões de Memória em Chatbots

## Introdução
Memória em chatbots é essencial para manter contexto em conversas longas e fornecer respostas coerentes. Este documento resume os principais padrões de implementação de memória usando **LangChain**.

---

## 1. Tipos de Memória

### 1.1 Memória de Curto Prazo (Short-Term Memory)
- **Descrição**: Armazena informações temporárias durante uma única sessão.
- **Uso**: Ideal para manter contexto imediato (ex.: histórico da conversa atual).
- **Implementação**:
  ```python
  from langchain.memory import ConversationBufferMemory

  memory = ConversationBufferMemory()
  memory.save_context({"input": "Olá!"}, {"output": "Como posso ajudar?"})
  ```

### 1.2 Memória de Longo Prazo (Long-Term Memory)
- **Descrição**: Persiste dados além da sessão atual (ex.: banco de dados, arquivos).
- **Uso**: Para armazenar preferências do usuário ou histórico de interações.
- **Implementação**:
  ```python
  from langchain.memory import ConversationSummaryMemory
  from langchain.chains import ConversationChain

  # Usa um LLM para resumir o histórico
  memory = ConversationSummaryMemory(llm=llm)
  chain = ConversationChain(llm=llm, memory=memory)
  ```

### 1.3 Memória Híbrida
- **Descrição**: Combina curto e longo prazo (ex.: buffer + sumário).
- **Implementação**:
  ```python
  from langchain.memory import ConversationBufferWindowMemory

  memory = ConversationBufferWindowMemory(k=3)  # Mantém últimos 3 diálogos
  ```

---

## 2. Padrões Comuns

### 2.1 Buffer de Conversação
- **Caso de uso**: Manter todo o histórico da conversa.
- **Vantagem**: Simples e direto.
- **Limitação**: Consome tokens rapidamente em conversas longas.

### 2.2 Sumarização de Conversação
- **Caso de uso**: Reduzir uso de tokens em diálogos extensos.
- **Exemplo**:
  ```python
  from langchain.memory import ConversationSummaryBufferMemory

  memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
  ```

### 2.3 Memória por Usuário
- **Caso de uso**: Personalização por usuário (ex.: preferências).
- **Implementação**:
  ```python
  from langchain.memory import MongoDBChatMessageHistory

  history = MongoDBChatMessageHistory(
      connection_string="mongodb://...",
      session_id="user123"
  )
  ```

---

## 3. Integração com LangChain

### 3.1 Usando `ConversationChain`
```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)

response = chain.run("Qual o clima hoje?")
print(response)  # Resposta com contexto
```

### 3.2 Usando `load_memory_variables`
```python
print(memory.load_memory_variables({}))
# Retorna: {'history': 'Humano: Olá!\nAI: Como posso ajudar?'}
```

---

## 4. Boas Práticas
1. **Limite de tokens**: Use `ConversationSummaryBufferMemory` para diálogos longos.
2. **Persistência**: Armazene memória em bancos de dados (ex.: Redis, MongoDB).
3. **Privacidade**: Evite armazenar dados sensíveis em memória.

---

## 5. Referências
- [Documentação LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [Tipos de Memória em LangChain](https://python.langchain.com/docs/modules/memory/types/)
```
```markdown
# Resumo Mês 2: Memória, Parsers e...

## Memória em LangChain
- **Tipos de memória**:
  - `ConversationBufferMemory`: Armazena todas as mensagens da conversa.
  - `ConversationSummaryMemory`: Resume a conversa para economizar contexto.
  - `ConversationBufferWindowMemory`: Mantém apenas as últimas `k` interações.
- **Uso prático**:
  ```python
  from langchain.memory import ConversationBufferMemory
  memory = ConversationBufferMemory(return_messages=True)
  ```

## Parsers e Output Processing
- **Formatos de saída**:
  - `StrOutputParser`: Extrai texto puro.
  - `JsonOutputParser`: Para respostas estruturadas.
  - `PydanticOutputParser`: Valida saída com um schema Pydantic.
- **Exemplo com JSON**:
  ```python
  from langchain.output_parsers import JsonOutputParser
  parser = JsonOutputParser()
  ```

## Integração com Ferramentas
- **Chamadas de ferramentas**:
  - Use `Tool` para funções externas (ex: busca na web).
  - Exemplo:
    ```python
    from langchain.tools import tool
    @tool
    def busca_web(query: str) -> str:
        """Busca na web."""
        return "Resultado..."
    ```

## Boas Práticas
- **Cache**: Use `InMemoryCache` para evitar chamadas repetidas.
- **Logs**: Habilite logs com `langchain.debug = True`.
- **Erros**: Trate exceções em cadeias (`try/except` em `Runnable`).
```
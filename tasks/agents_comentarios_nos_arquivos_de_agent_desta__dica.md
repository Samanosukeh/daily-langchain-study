```markdown
# Dicas Rápidas: Comentários em Arquivos de Agentes LangChain

## 1. **Comentários de Linha Única**
Use `#` para comentários rápidos:
```python
# Este é um comentário de linha única
agent = initialize_agent(...)  # Inicializa o agente
```

## 2. **Docstrings para Funções**
Documente funções com `"""..."""`:
```python
def load_tool(tool_name: str) -> Tool:
    """Carrega uma ferramenta específica pelo nome.

    Args:
        tool_name (str): Nome da ferramenta (e.g., "serpapi").

    Returns:
        Tool: Instância da ferramenta carregada.
    """
    return load_toolkit(tool_name)
```

## 3. **Comentários de Bloco**
Use `"""` para comentários multi-linha:
```python
"""
Configuração do agente:
- Ferramentas: SerpAPI, Wikipedia
- Modelo: ChatOpenAI
- Verbosidade: True
"""
agent = Agent(tools=[serpapi, wikipedia], model=model, verbose=True)
```

## 4. **Comentários em YAML/JSON**
Em arquivos de configuração (e.g., `langchain.yaml`):
```yaml
# Chave API para o modelo (evite hardcoding)
api_key: ${OPENAI_API_KEY}  # Carregada do ambiente
```

## 5. **Dicas Práticas**
- **Evite comentários óbvios**: Prefira código claro.
- **Comente decisões complexas**: Ex.: `# Usamos `RunnablePassthrough` para passar contexto`.
- **Ferramentas de Lint**: Use `flake8` ou `pylint` para validar comentários.

## 6. **Exemplo Prático**
```python
# Configura o agente com memória e ferramentas
agent = Agent(
    tools=[search_tool],  # Ferramenta de busca
    memory=ConversationBufferMemory(),  # Memória de conversa
    # verbose=True  # Descomentar para debug
)
```
```
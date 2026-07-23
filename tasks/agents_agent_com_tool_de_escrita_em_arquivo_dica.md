```markdown
# Dicas Rápidas: Agent com Tool de Escrita em Arquivos

## Configuração Inicial
```python
from langchain.agents import AgentType, initialize_agent
from langchain.tools import FileManagementToolkit
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
tools = FileManagementToolkit().get_tools()
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

## Ferramentas Essenciais
- `list_directory`: Lista arquivos/diretórios
- `read_file`: Lê conteúdo de arquivo
- `write_file`: Escreve/cria arquivo
- `delete_file`: Remove arquivo
- `search_files`: Busca por nome/padrão

## Boas Práticas
1. **Valide permissões**: Verifique se o agente tem acesso ao diretório alvo
2. **Trate erros**: Implemente `try/except` para operações de arquivo
3. **Limite escopo**: Restrinja o diretório de trabalho com `root_dir`

## Exemplo de Uso
```python
response = agent.run(
    "Crie um arquivo 'notas.txt' com 'Reunião às 14h' no diretório atual"
)
```

## Segurança
- Evite usar `*` em caminhos de arquivos
- Restrinja permissões do processo
- Valide extensões de arquivo
```
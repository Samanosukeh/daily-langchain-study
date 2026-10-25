```markdown
# Reflexão: CLI Simples para Interagir com um Sistema de IA

Construir uma CLI para um sistema de IA exige equilíbrio entre simplicidade e flexibilidade. O desafio está em abstrair a complexidade dos modelos (como LangChain) sem limitar o usuário avançado.

Optei por usar `argparse` para parsing de argumentos, pois é nativo e evita dependências desnecessárias. A hierarquia de comandos deve ser intuitiva:
- `/chat` para interação conversacional
- `/search` para buscas em documentos
- `/config` para ajustes de parâmetros

A integração com LangChain é direta: cada comando mapeia para uma cadeia (`chain`) ou ferramenta (`tool`). Exemplo:
```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)
```

O maior problema é gerenciar estado entre chamadas. Solução: usar `prompt_toolkit` para history e persistência de contexto em arquivo JSON. Para saída, formatação em Markdown via `rich` melhora legibilidade.

Performance não é crítica aqui, mas evitar recriar cadeias a cada execução é crucial. Cache em memória com `functools.lru_cache` ajuda, mas para CLI local, um simples `singleton` já resolve.

Próximo passo: adicionar suporte a múltiplos LLMs via configuração YAML e validação de schemas com `pydantic`.
```
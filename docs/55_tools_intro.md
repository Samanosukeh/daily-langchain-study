```markdown
# Tools em LangChain

## Introdução
Tools (ferramentas) são componentes essenciais em LangChain que permitem que modelos de linguagem interajam com o mundo externo. Elas estendem a capacidade dos LLMs além do processamento de texto puro, possibilitando ações como buscar informações, executar código ou interagir com APIs.

## Conceito Básico
- **Definição**: Uma Tool é uma função que recebe uma string de entrada e retorna uma string de saída.
- **Interface Padrão**:
  ```python
  from typing import Optional, Type

  class BaseTool:
      name: str
      description: str
      args_schema: Optional[Type[BaseModel]] = None

      def _run(self, *args: Any, **kwargs: Any) -> str:
          raise NotImplementedError

      async def _arun(self, *args: Any, **kwargs: Any) -> str:
          raise NotImplementedError
  ```
- **Métodos Essenciais**:
  - `_run()`: Execução síncrona
  - `_arun()`: Execução assíncrona (opcional mas recomendado)

## Tipos Comuns de Tools

### 1. Ferramentas de Busca
```python
from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
resultado = search.run("Últimas notícias sobre IA em 2024")
```

### 2. Ferramentas de Código
```python
from langchain.tools import PythonREPLTool

python_repl = PythonREPLTool()
resultado = python_repl.run("print(2+2)")
```

### 3. Ferramentas de API
```python
from langchain.tools import APIOperation

api_tool = APIOperation(
    name="get_github_user",
    description="Busca informações de um usuário do GitHub",
    method="GET",
    url="https://api.github.com/users/{username}"
)
```

### 4. Ferramentas Personalizadas
```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    a: float = Field(description="Primeiro número")
    b: float = Field(description="Segundo número")

class CalculatorTool(BaseTool):
    name = "calculadora"
    description = "Calcula operações matemáticas básicas"
    args_schema = CalculatorInput

    def _run(self, a: float, b: float, operation: str = "soma") -> str:
        if operation == "soma":
            return str(a + b)
        elif operation == "subtração":
            return str(a - b)
        # ... outras operações

calculadora = CalculatorTool()
resultado = calculadora.run(a=5, b=3, operation="soma")
```

## Integração com Agents
Tools são usadas pelos Agents para executar ações:

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
tools = [DuckDuckGoSearchRun(), CalculatorTool()]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent.run("Quanto é 10 elevado ao quadrado?")
```

## Boas Práticas

1. **Descrição Clara**: Sempre documente o propósito e uso da tool
2. **Tratamento de Erros**: Implemente validação robusta de entrada
3. **Performance**: Para tools lentas, considere cache ou execução assíncrona
4. **Segurança**: Nunca exponha tools sensíveis sem autenticação adequada

## Ferramentas Pré-construídas

LangChain oferece diversas tools prontas:
- `SerpAPI` (Busca na web)
- `Wikipedia` (Busca na Wikipédia)
- `GoogleSerperAPIWrapper`
- `WolframAlpha` (Cálculos avançados)
- `FileSystem` (Leitura/escrita de arquivos)

## Personalização Avançada

Para tools complexas:
```python
from langchain.tools import StructuredTool

def buscar_preco_produto(produto: str) -> str:
    # Lógica de busca em banco de dados ou API
    return f"R$ 199,90"

busca_preco = StructuredTool.from_function(
    func=buscar_preco_produto,
    name="BuscaPrecoProduto",
    description="Busca o preço atual de um produto"
)
```

## Considerações Finais
- Tools devem ser idempotentes quando possível
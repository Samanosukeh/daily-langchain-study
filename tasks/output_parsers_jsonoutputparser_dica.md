```markdown
# JsonOutputParser: Retorno em JSON com LangChain

## Configuração Básica

```python
from langchain.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

parser = JsonOutputParser(pydantic_object=SeuModeloPydantic)
```

## Definindo o Schema

```python
class Filme(BaseModel):
    titulo: str = Field(description="Título do filme")
    ano: int = Field(description="Ano de lançamento")
    genero: list[str] = Field(description="Lista de gêneros")
```

## Usando no Prompt

```python
prompt = PromptTemplate(
    template="Extraia as informações do filme:\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

## Executando a Extração

```python
chain = prompt | llm | parser
resultado = chain.invoke({"query": "O Senhor dos Anéis, lançado em 2001, gêneros: fantasia, aventura"})
```

## Tratando Erros

```python
try:
    dados = parser.parse(resultado)
except Exception as e:
    print(f"Erro no parsing: {e}")
```

## Dicas Rápidas

- Use `Field` para adicionar descrições aos campos
- Valide o schema com `pydantic_object`
- Formate instruções com `get_format_instructions()`
- Teste com exemplos simples antes de casos complexos
```
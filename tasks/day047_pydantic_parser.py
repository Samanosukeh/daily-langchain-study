```markdown
# Comentários e Docstrings nos Output Parsers

## Introdução
Os `output_parsers` no LangChain são responsáveis por estruturar a saída bruta de modelos de linguagem (LLMs) em formatos úteis para aplicações. A documentação e comentários são essenciais para manter a clareza e facilitar a manutenção do código.

---

## 1. Comentários em Parsers

### Boas Práticas
- **Clareza**: Comentários devem explicar **por que** o código existe, não apenas o que faz.
- **Contexto**: Incluir exemplos de entrada/saída quando relevante.
- **Atualização**: Manter comentários alinhados com mudanças no código.

### Exemplo Prático
```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# Define os schemas de resposta para o parser estruturado.
# Cada schema mapeia um campo do JSON de saída esperado.
response_schemas = [
    ResponseSchema(name="nome", description="Nome do usuário"),
    ResponseSchema(name="idade", description="Idade do usuário em anos"),
]

# Inicializa o parser com os schemas definidos.
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Obtém o formato de instrução para incluir no prompt.
# Isso instrui o LLM a retornar a saída no formato esperado.
format_instructions = output_parser.get_format_instructions()

# Template do prompt com instruções de formato.
prompt_template = PromptTemplate(
    template="Extraia as seguintes informações do texto:\n{format_instructions}\n{texto}",
    input_variables=["texto"],
    partial_variables={"format_instructions": format_instructions}
)

# Exemplo de uso:
texto = "João tem 30 anos."
prompt = prompt_template.format(texto=texto)

llm = OpenAI(temperature=0)
output = llm.predict(prompt)

# Faz o parsing da saída bruta do LLM para um dicionário Python.
parsed_output = output_parser.parse(output)
print(parsed_output)  # {'nome': 'João', 'idade': '30'}
```

> **Comentário**:
> O `StructuredOutputParser` é útil quando você precisa garantir que a saída do LLM seja sempre um JSON válido com campos específicos.
> Aqui, extraímos `nome` e `idade` de um texto livre. O `format_instructions` é crucial para guiar o LLM a retornar a estrutura correta.

---

## 2. Docstrings em Parsers

Docstrings devem seguir o padrão [PEP 257](https://peps.python.org/pep-0257/) e incluir:

1. **Descrição curta**: Uma linha resumindo o propósito do parser.
2. **Descrição longa**: Detalhes sobre como o parser funciona, exemplos de uso e parâmetros.
3. **Args**: Documentação de cada parâmetro.
4. **Returns**: Estrutura e tipo de retorno.
5. **Exemplo**: Uso prático com entrada e saída.

### Exemplo: Docstring para `StructuredOutputParser`

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class StructuredOutputParser:
    """
    Um parser para converter saídas brutas de LLMs em estruturas de dados Python.

    Este parser é especialmente útil quando você precisa garantir que a saída do LLM
    siga um esquema específico (ex: JSON com campos pré-definidos). Ele é comumente
    usado com `PromptTemplate` para instruir o LLM a retornar dados em um formato estruturado.

    Attributes:
        response_schemas (List[ResponseSchema]): Lista de schemas que definem a estrutura da saída.
        pydantic_model (BaseModel): Modelo Pydantic gerado a partir dos schemas.

    Args:
        response_schemas (List[ResponseSchema]): Lista de objetos `ResponseSchema` que descrevem
            cada campo da saída esperada. Cada schema deve ter `name` (nome do campo) e
            `description` (descrição do campo).
        **kwargs: Argumentos adicionais para o modelo Pydantic (ex: `Config`).

    Returns:
        Dict[str, Any]: Um dicionário Python com os campos extraídos da saída do LLM.

    Example:
        >>> from langchain.output_parsers import ResponseSchema
        >>> schemas = [
        ...     ResponseSchema(name="ativo", description="Se o usuário está ativo"),
        ...     ResponseSchema(name="email", description="Endereço de email do usuário"),
        ... ]
        >>> parser = Struct
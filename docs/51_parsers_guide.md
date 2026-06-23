```markdown
# Resumo: Quando Usar Cada Output Parser

## Visão Geral
Os `OutputParsers` em LangChain são responsáveis por transformar a saída bruta de modelos de linguagem (LLMs) em estruturas de dados úteis para sua aplicação. A escolha do parser adequado depende do formato de saída esperado e do uso pretendido.

---

## Tabela Comparativa de Output Parsers

| **Parser**               | **Uso Principal**                                                                 | **Formato de Saída**                     | **Caso de Uso Típico**                          | **Vantagens**                          | **Limitações**                          |
|--------------------------|-----------------------------------------------------------------------------------|------------------------------------------|------------------------------------------------|----------------------------------------|------------------------------------------|
| `StrOutputParser`        | Quando a saída é um texto simples ou não requer estruturação.                     | String pura (`str`)                      | Respostas diretas, logs, ou texto não estruturado. | Simples, sem dependências.             | Não lida com estruturas complexas.      |
| `JsonOutputParser`       | Quando a saída do LLM é um JSON válido.                                           | Dicionário Python (`dict`)               | APIs, configurações, ou dados estruturados.    | Fácil de integrar com sistemas JSON.   | Requer que o LLM gere JSON válido.      |
| `PydanticOutputParser`   | Quando a saída deve seguir um schema Pydantic (validação de tipos e campos).      | Instância de uma classe Pydantic.        | Dados fortemente tipados (ex: configurações).  | Validação automática de tipos.         | Requer definição prévia do schema.      |
| `ListOutputParser`       | Quando a saída é uma lista de itens (ex: múltiplos resultados).                   | Lista Python (`list`)                    | Extração de múltiplos itens, como tópicos.      | Fácil manipulação de listas.           | Não valida conteúdo dos itens.          |
| `CommaSeparatedListOutputParser` | Quando a saída é uma lista separada por vírgulas.                          | Lista Python (`list`)                    | Entradas simples como tags ou categorias.      | Sintaxe simples para o LLM.           | Não lida com itens contendo vírgulas.   |
| `MarkdownHeaderTextSplitter` | Quando a saída é um markdown com seções hierárquicas.                     | Lista de dicionários (seções + texto).   | Processamento de documentos markdown.          | Preserva estrutura de seções.          | Requer formatação específica do LLM.    |
| `StructuredOutputParser` | Quando a saída deve seguir um schema definido (mistura de tipos e validações).    | Dicionário Python (`dict`)               | Saídas complexas com múltiplos campos.         | Flexível e validado.                   | Requer definição detalhada do schema.   |
| `CustomOutputParser`     | Quando nenhuma solução padrão atende às necessidades específicas.                 | Qualquer estrutura personalizada.        | Lógica de parsing customizada.                 | Totalmente adaptável.                  | Requer implementação manual.            |

---

## Quando Usar Cada Parser

### 1. **`StrOutputParser`**
- **Use quando:**
  - A saída do LLM é um texto simples (ex: resposta a uma pergunta aberta).
  - Você não precisa de estrutura ou validação.
  - Exemplo:
    ```python
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_template("Diga-me uma piada sobre {tema}.")
    model = ChatOpenAI()
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    result = chain.invoke({"tema": "programação"})
    print(result)  # Saída: string pura
    ```

---

### 2. **`JsonOutputParser`**
- **Use quando:**
  - A saída do LLM é um JSON válido (ex: APIs, configurações).
  - Você precisa de uma estrutura de dicionário para processamento posterior.
  - Exemplo:
    ```python
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_template(
        "Extraia as informações a seguir em formato JSON: {texto}. "
        "Responda apenas com o JSON."
    )
    model = ChatOpenAI()
    output_parser = Json
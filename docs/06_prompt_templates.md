```markdown
# O que são PromptTemplates

## Definição
`PromptTemplate` é uma classe do LangChain que padroniza a criação de prompts para modelos de linguagem. Ela permite definir estruturas reutilizáveis para inputs dinâmicos, facilitando a manutenção e consistência dos prompts.

## Características Principais
- **Estrutura reutilizável**: Define um template com variáveis substituíveis.
- **Flexibilidade**: Suporta inputs dinâmicos via parâmetros.
- **Integração**: Compatível com `LLMChain`, `RetrievalQA`, entre outros.

## Sintaxe Básica
```python
from langchain.prompts import PromptTemplate

template = """Pergunta: {pergunta}
Contexto: {contexto}
Resposta:"""

prompt = PromptTemplate(
    input_variables=["pergunta", "contexto"],
    template=template
)
```

## Parâmetros
| Parâmetro       | Tipo       | Descrição                          |
|-----------------|------------|------------------------------------|
| `input_variables` | `list[str]` | Variáveis a serem preenchidas.    |
| `template`      | `str`      | Texto com placeholders (`{var}`).  |
| `template_format` | `str` (opcional) | Formato do template (`f-string` ou `jinja2`). |

## Exemplo Prático
```python
prompt = PromptTemplate(
    input_variables=["tarefa", "prioridade"],
    template="Execute a tarefa '{tarefa}' com prioridade {prioridade}."
)

formatted_prompt = prompt.format(
    tarefa="revisão de código",
    prioridade="alta"
)
# Saída: "Execute a tarefa 'revisão de código' com prioridade alta."
```

## Boas Práticas
1. **Nomes descritivos**: Use nomes claros para variáveis (ex: `{pergunta}` em vez de `{q}`).
2. **Validação**: Verifique se todos os placeholders são preenchidos antes de usar o prompt.
3. **Versionamento**: Mantenha templates em arquivos separados para reuso.

## Avançado: Partial Templates
Preencha partes do template antecipadamente:
```python
partial_prompt = prompt.partial(contexto="Documentação oficial do LangChain")
```

## Referência
- [Documentação Oficial](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/)
```
```markdown
# Dicas Rápidas: Tools em LangChain

## Conceito Básico
- **Tools** são funções ou APIs externas que o LLM pode usar para realizar ações específicas.
- Permitem que modelos de linguagem interajam com sistemas reais (bancos de dados, APIs, etc.).

## Principais Características
- **Interface Padronizada**: Todas as tools seguem o padrão `name`, `description` e `func`.
- **Invocação Dinâmica**: O LLM decide quando e qual tool usar com base na descrição fornecida.
- **Retorno Estruturado**: Tools retornam dados em formato compatível para o LLM (ex: JSON).

## Implementação Básica
```python
from langchain.agents import tool

@tool
def buscar_clima(cidade: str) -> str:
    """Busca a temperatura atual de uma cidade"""
    # Lógica de chamada à API
    return f"Temperatura em {cidade}: 25°C"

tools = [buscar_clima]
```

## Boas Práticas
1. **Descrições Claras**: Use descrições detalhadas para ajudar o LLM a entender quando usar a tool.
2. **Tratamento de Erros**: Implemente validação de entrada e tratamento de exceções.
3. **Performance**: Cache resultados frequentes para evitar chamadas desnecessárias.
4. **Segurança**: Valide inputs para prevenir injeção de código ou SQL.

## Tools Comuns
- **APIs Externas**: Google Search, Wikipedia, APIs de clima.
- **Funções Internas**: Busca em banco de dados, cálculos matemáticos.
- **Integrações**: Slack, Notion, GitHub.

## Debugging
- Use `print` ou logging para monitorar chamadas de tools.
- Verifique logs do agente para entender decisões do LLM.
- Teste tools isoladamente antes de integrá-las ao agente.

## Ferramentas Úteis
- `langchain.tools`: Biblioteca padrão com tools prontas.
- `langchain.agents`: Estruturas para criar agentes com tools.
```
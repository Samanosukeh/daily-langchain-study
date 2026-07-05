```markdown
# Tool de Calculadora em LangChain: Operações Básicas

## Configuração Inicial
```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

@tool
def calculadora(expressao: str) -> float:
    """Executa operações matemáticas básicas (+, -, *, /)"""
    try:
        return eval(expressao)
    except:
        raise ValueError("Expressão inválida")
```

## Inicialização do Agente
```python
agent = initialize_agent(
    tools=[calculadora],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

## Exemplos de Uso
```python
# Soma
agent.run("Quanto é 15 + 27?")

# Multiplicação
agent.run("Calcule 8 * 9.5")

# Divisão com casas decimais
agent.run("Divida 100 por 3 e arredonde para 2 casas")

# Operações encadeadas
agent.run("Some 5 e 3, depois multiplique por 2")
```

## Dicas Práticas
1. **Validação**: Sempre valide a entrada para evitar injeção de código
2. **Precisão**: Para cálculos financeiros, use `decimal.Decimal`
3. **Erros**: Trate exceções para expressões inválidas
4. **Segurança**: Restrinja operações permitidas em ambientes produtivos
5. **Desempenho**: Cache resultados de cálculos repetitivos

## Limitações
- Não substitui bibliotecas matemáticas especializadas
- Avalia expressões com `eval()` (risco em produção)
- Operações complexas podem exceder limites do LLM
```
```markdown
# Notas Técnicas: Chains Avançados em LangChain – Controle de Fluxo com `RouterChain`

## Contexto
As `RouterChain` permitem direcionar dinamicamente a execução de cadeias (`Chains`) com base em condições pré-definidas. Embora menos documentadas que as `LLMChain`, são essenciais para sistemas que exigem lógica condicional avançada.

---

## Implementação Básica

### 1. Definição de Rotas
Crie um dicionário de rotas com condições (`condition`) e cadeias (`chain`) associadas:
```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate

destinations = [
    "matematica",
    "ciencia",
    "historia"
]
destinations_descriptions = [
    "Questões envolvendo cálculos ou álgebra.",
    "Questões sobre física, química ou biologia.",
    "Questões sobre eventos históricos ou datas."
]
```

### 2. Criação do Roteador
Use `LLMRouterChain` para classificar consultas:
```python
default_prompt = PromptTemplate.from_template(
    "Responda de forma genérica: {input}"
)
router_template = """Dado uma pergunta de usuário, classifique-a como uma das seguintes categorias:
{destinations}

Formato esperado:
{format_instructions}

Pergunta: {input}"""

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    partial_variables={
        "destinations": "\n".join(destinations),
        "format_instructions": RouterOutputParser().get_format_instructions()
    }
)
router_chain = LLMRouterChain.from_llm(
    llm=llm,
    prompt=router_prompt
)
```

### 3. Integração com `MultiPromptChain`
Encadeie o roteador com cadeias especializadas:
```python
from langchain.chains import ConversationChain

chains = {}
for dest in destinations:
    chains[dest] = ConversationChain.from_llm(llm=llm)

chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=chains,
    default_chain=default_prompt,
    verbose=True
)
```

---

## Validação e Debug
- **Teste de Roteamento**: Verifique se consultas são direcionadas corretamente:
  ```python
  result = chain.run("Qual a capital do Brasil?")
  assert "historia" in result  # Deve ser roteado para história
  ```
- **Logs Verbosos**: Ative `verbose=True` para inspecionar decisões do roteador.

---

## Casos de Uso
- **Sistemas de Suporte Técnico**: Direcione perguntas para equipes especializadas.
- **Chatbots Educacionais**: Separe tópicos por disciplina.
- **Fallback Seguro**: Use `default_chain` para consultas não mapeadas.

---

## Limitações
- **Dependência do LLM**: A precisão do roteamento depende da qualidade do modelo.
- **Complexidade**: Adiciona camada de abstração que pode obscurecer erros.
```
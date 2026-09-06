```markdown
# Chains Avançadas: RouterChain e MultiPromptChain

## RouterChain

A `RouterChain` permite rotear a entrada do usuário para diferentes cadeias (`chains`) com base em critérios pré-definidos (ex: tipo de pergunta, intenção, etc.). É útil para sistemas que precisam direcionar consultas complexas para especialistas distintos.

### Implementação Básica

```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate

# Definir os prompts especializados
physics_template = """Você é um físico especializado em mecânica quântica..."""
math_template = """Você é um matemático especializado em álgebra linear..."""

# Criar o roteador
destination_prompts = {
    "física": PromptTemplate.from_template(physics_template),
    "matemática": PromptTemplate.from_template(math_template),
}
default_prompt = PromptTemplate.from_template("Responda de forma genérica.")
router_template = """Dado uma pergunta, roteie para a cadeia especializada apropriada:
{input}"""

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(destination_prompts.keys()),
)

# Criar o roteador LLM
router_chain = LLMRouterChain.from_llm(
    llm,
    router_prompt,
    destination_prompts,
    default_prompt,
)

# Criar a MultiPromptChain
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_prompts,
    default_chain=default_prompt,
    verbose=True,
)
```

### Parâmetros-Chave
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `router_chain` | `LLMRouterChain` | Define as regras de roteamento. |
| `destination_chains` | `dict` | Cadeias especializadas mapeadas por rótulo. |
| `default_chain` | `Chain` | Cadeia genérica para casos não roteados. |
| `verbose` | `bool` | Exibe logs detalhados (padrão: `False`). |

---

## MultiPromptChain

Extensão da `RouterChain` que permite combinar múltiplos prompts especializados em uma única cadeia. Ideal para sistemas com domínios múltiplos (ex: suporte técnico com categorias como "hardware", "software", etc.).

### Implementação

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Definir prompts especializados
hardware_prompt = PromptTemplate.from_template("Você é um técnico de hardware...")
software_prompt = PromptTemplate.from_template("Você é um técnico de software...")

# Criar destinos
destination_chains = {
    "hardware": ConversationChain(
        llm=llm,
        prompt=hardware_prompt,
        memory=ConversationBufferMemory(),
    ),
    "software": ConversationChain(
        llm=llm,
        prompt=software_prompt,
        memory=ConversationBufferMemory(),
    ),
}

# Configurar roteador (mesmo modelo da RouterChain)
router_chain = LLMRouterChain.from_llm(
    llm,
    router_prompt,
    destination_chains,
    default_prompt,
)

# Criar MultiPromptChain
multi_prompt_chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=ConversationChain(
        llm=llm,
        prompt=default_prompt,
        memory=ConversationBufferMemory(),
    ),
    verbose=True,
)
```

### Exemplo de Uso

```python
# Pergunta roteada para "hardware"
response = multi_prompt_chain.run("Meu teclado não está funcionando!")
print(response)  # Resposta do técnico de hardware

# Pergunta roteada para "software"
response = multi_prompt_chain.run("Como instalar o Python?")
print(response)  # Resposta do técnico de software
```

### Casos de Uso
- **Suporte Técnico**: Roteamento por tipo de problema.
- **Assistentes Virtuais**: Direcionamento por intenção do usuário.
- **Sistemas de Perguntas Frequentes**: Categorização automática de dúvidas.

---

## Boas Práticas

1. **Prompt Engineering**:
   - Use exemplos claros no `router_prompt` para melhorar a acurácia do roteamento.
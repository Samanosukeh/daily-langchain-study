```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate

# Definir prompts especializados
physics_template = """Você é um especialista em física. \
Responda apenas questões relacionadas à física.

{input}"""

math_template = """Você é um especialista em matemática. \
Responda apenas questões relacionadas à matemática.

{input}"""

history_template = """Você é um especialista em história. \
Responda apenas questões relacionadas à história.

{input}"""

# Criar prompts a partir das templates
physics_prompt = PromptTemplate.from_template(physics_template)
math_prompt = PromptTemplate.from_template(math_template)
history_prompt = PromptTemplate.from_template(history_template)

# Definir destinos para o roteamento
destinations = [
    "física: questões relacionadas à física",
    "matemática: questões relacionadas à matemática",
    "história: questões relacionadas à história"
]

# Definir instruções de roteamento
default_instruction = """Dado um input de usuário, escolha a cadeia mais adequada para responder à questão.
Seguem as cadeias disponíveis e quando usá-las:

{destinations}

Exemplo de input: "Quem foi Isaac Newton?"
Saída: "história"

Input: {input}
Saída:"""

router_prompt = PromptTemplate(
    template=default_instruction,
    input_variables=["input", "destinations"],
    output_parser=RouterOutputParser(),
)

# Inicializar o roteador
router_chain = LLMRouterChain.from_llm(
    llm=modelo_llm,
    prompt=router_prompt,
    output_parser=RouterOutputParser(),
)

# Criar cadeias especializadas
physics_chain = LLMChain(llm=modelo_llm, prompt=physics_prompt)
math_chain = LLMChain(llm=modelo_llm, prompt=math_prompt)
history_chain = LLMChain(llm=modelo_llm, prompt=history_prompt)

# Definir cadeias especializadas em um dicionário
destination_chains = {
    "física": physics_chain,
    "matemática": math_chain,
    "história": history_chain
}

# Criar a MultiPromptChain com roteamento
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=history_chain,  # cadeia padrão se nenhuma rota for identificada
    verbose=True
)

# Testar o roteamento
input_usuario = "Qual é a fórmula da energia cinética?"
resposta = chain.run(input_usuario)
print(resposta)

input_usuario = "Quem descobriu a gravidade?"
resposta = chain.run(input_usuario)
print(resposta)

input_usuario = "Qual é o teorema de Pitágoras?"
resposta = chain.run(input_usuario)
print(resposta)
```
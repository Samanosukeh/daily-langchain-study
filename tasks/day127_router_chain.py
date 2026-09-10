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

---

```markdown
# Comentários nas Chains Avançadas

## Introdução
Em chains avançadas do LangChain, comentários são essenciais para documentar fluxos complexos, facilitar a manutenção e melhorar a colaboração. Utilize comentários inline e blocos para explicar lógica, decisões e fluxos não óbvios.

---

## 1. Comentários Inline
Adicione comentários ao lado de trechos críticos para explicar a lógica ou propósito.

### Exemplo Básico
```python
from langchain_core.runnables import RunnablePassthrough

# Define um passo para extrair o 'texto' do input
extract_text = lambda x: x["texto"]

# Comentar sobre a transformação seguinte
processed_text = (
    {"texto": RunnablePassthrough()}  # Input original
    | extract_text  # Extrai o campo 'texto'
    | {"texto_processado": lambda x: x.upper()}  # Converte para maiúsculas
)
```

### Exemplo com LLM
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Comentário: Prompt para análise de sentimento
prompt = ChatPromptTemplate.from_template(
    """Analise o sentimento do texto abaixo.
    Retorne apenas 'positivo', 'negativo' ou 'neutro'.

    Texto: {texto}
    """
)

# Comentário: Instancia o modelo com configurações específicas
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.3,  # Baixa temperatura para respostas mais determinísticas
)

# Comentário: Chain para processar texto e retornar sentimento
sentiment_chain = prompt | model
```

---

## 2. Comentários em Blocos
Use blocos de comentários (`""" """` ou `#`) para explicar seções inteiras ou lógica complexa.

### Exemplo: Chain com Condicional
```python
from langchain_core.output_parsers import StrOutputParser

# =============================================
# Chain para roteamento de perguntas:
# - Se a pergunta for sobre 'preço', responde com preço.
# - Se for sobre 'estoque', responde com estoque.
# - Caso contrário, responde genericamente.
# =============================================
def route_question(input_data):
    pergunta = input_data.get("pergunta", "").lower()

    if "preço" in pergunta:
        return "O preço do produto é R$ 199,90."
    elif "estoque" in pergunta:
        return "O estoque atual é de 50 unidades."
    else:
        return "Não entendi sua pergunta. Tente 'preço' ou 'estoque'."

# Comentário: Define a chain principal
chain = (
    {"pergunta": RunnablePassthrough()}
    | route_question  # Roteia a pergunta
    | StrOutputParser()  # Converte saída para string
)
```

---

## 3. Comentários em Configurações de Chains
Documente parâmetros e configurações para facilitar ajustes futuros.

### Exemplo: Configuração de RAG
```python
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import FakeEmbeddings

# =============================================
# Configuração do Retriever RAG:
# - Embeddings: FakeEmbeddings (para exemplo)
# - Vector Store: FAISS (similaridade por cosseno)
# - k=3: Retorna top 3 documentos mais similares
# =============================================
embeddings = FakeEmbeddings(size=128)
vector_store = FAISS.from_texts(
    ["Exemplo de documento 1", "Exemplo de documento 2"],
    embeddings,
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Comentário: Chain de RAG
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | {"response": lambda x: x["question"]}  # Simplificação para exemplo
)
```

---

## 4. Boas Práticas
1. **Seja específico**: Evite comentários genéricos como `# Processa os dados`. Prefira:
   ```python
   # Extrai e normaliza o campo 'nome' para minúsculas
   normalized_name = (input_data["nome"] or "").strip().lower()
   ```

2. **Documente decisões de design**:
   ```python
   # Usamos temperatura=0.7 para equilibrar criatividade e coerência nas respostas
   model = ChatOpenAI(temperature
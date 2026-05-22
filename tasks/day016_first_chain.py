```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Definindo o prompt template
prompt = ChatPromptTemplate.from_template(
    "Resuma o seguinte texto em uma única frase: {text}"
)

# Inicializando o modelo de linguagem
llm = ChatOpenAI(model="gpt-4o-mini")

# Criando a chain usando LCEL
chain = prompt | llm | StrOutputParser()

# Executando a chain com um input
input_text = "A linguagem Python foi criada por Guido van Rossum em 1991. É uma linguagem de programação de alto nível, interpretada e de propósito geral."
result = chain.invoke({"text": input_text})

print(result)
```

---

```markdown
# Comentários Detalhados na Chain LCEL

## Visão Geral
Este documento detalha o uso de comentários em chains LCEL (LangChain Expression Language) para melhorar a legibilidade, manutenção e documentação do código.

---

## Estrutura Básica de Comentários

### Comentários de Linha
```python
# Este é um comentário de linha em LCEL
prompt = ChatPromptTemplate.from_template("Diga-me um {adjetivo} piada sobre {tema}.")
```

### Comentários de Bloco
```python
"""
Este é um comentário de bloco.
Utilizado para explicar blocos de código complexos ou chains inteiras.
"""
chain = prompt | model | output_parser
```

---

## Comentários em Chains LCEL

### Comentários em Expressões de Pipeline
```python
# Define uma chain básica com pipeline (|)
chain = prompt | model | output_parser

# Comentário explicando a flow da chain
# prompt -> model -> output_parser
```

### Comentários em Funções de Chain
```python
def criar_chain_analise_texto():
    """
    Cria uma chain LCEL para análise de texto.

    Retorna:
        Chain: Uma chain LCEL pronta para uso.
    """
    # Define o prompt template
    prompt = ChatPromptTemplate.from_template(
        "Analise o seguinte texto e extraia as entidades mencionadas: {texto}"
    )

    # Comenta a lógica da chain
    chain = (
        prompt
        | model  # Envia o prompt ao modelo
        | StrOutputParser()  # Converte a saída em string
    )

    return chain
```

---

## Comentários em Componentes LCEL

### Comentários em Prompts
```python
prompt = ChatPromptTemplate.from_messages([
    # Mensagem do sistema para definir o comportamento do modelo
    ("system", "Você é um assistente útil que responde em português."),
    # Mensagem do usuário para receber a entrada
    ("user", "Resuma o seguinte texto: {texto}"),
])
```

### Comentários em Modelos
```python
# Carrega o modelo com configurações específicas
model = ChatOpenAI(
    model="gpt-4",  # Modelo utilizado
    temperature=0.7,  # Controla a criatividade das respostas
    max_tokens=1000,  # Limita o tamanho da resposta
)
```

### Comentários em Parsers
```python
# Define um parser para extrair dados estruturados
output_parser = JsonOutputParser()

# Exemplo de uso do parser
# Saída esperada: {"entidades": ["Python", "LangChain"]}
```

---

## Comentários em Configurações Avançadas

### Comentários em Chains com Condicionais
```python
chain = (
    {
        "texto": lambda x: x["texto"],  # Extrai o campo 'texto'
        "lingua": lambda x: x["lingua"]  # Extrai o campo 'lingua'
    }
    | prompt  # Envia os campos extraídos ao prompt
    | model  # Processa pelo modelo
    | output_parser  # Converte a saída
)
```

### Comentários em Chains com Funções Customizadas
```python
def formatar_saida(output: str) -> str:
    """
    Formata a saída da chain para remover caracteres indesejados.

    Args:
        output (str): Saída bruta do modelo.

    Returns:
        str: Saída formatada.
    """
    # Remove caracteres especiais
    return output.replace("\n", " ").strip()

# Integra a função customizada na chain
chain = (
    prompt
    | model
    | StrOutputParser()
    | formatar_saida  # Aplica a função customizada
)
```

---

## Boas Práticas para Comentários em LCEL

1. **Seja Conciso**: Comentários devem explicar o "porquê" e não o "o que".
   ```python
   # ✅ Bom: Explica a razão da configuração
   model = ChatOpenAI(temperature=0.3)  # Baixa temperatura para respostas mais precisas
   ```

2. **Documente Funções e Classes**:
   ```python
   def criar_chain_analise_sentimento():
       """
       Cria uma chain LCEL para análise de sentimento em textos.

       Utiliza um modelo de linguagem para classificar o sentimento como:
       - Positivo
       - Neutro
       - Negativo

       Returns:
           Chain: Chain L
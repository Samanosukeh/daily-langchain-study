```python
from langchain_core.runnables import RunnableParallel

# Exemplo básico de RunnableParallel
# Executando dois ramos em paralelo e combinando os resultados

# Definindo dois ramos simples
branch_1 = {"input": lambda x: x["texto"].upper()}
branch_2 = {"input": lambda x: x["texto"].lower()}

# Criando o RunnableParallel
parallel_runnable = RunnableParallel(branch_1=branch_1, branch_2=branch_2)

# Executando com um input
input_data = {"texto": "Hello World"}
result = parallel_runnable.invoke(input_data)

print(result)
# Saída esperada: {'branch_1': {'input': 'HELLO WORLD'}, 'branch_2': {'input': 'hello world'}}

# Exemplo mais avançado com chamadas a modelos
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Modelo
model = ChatOpenAI(model="gpt-3.5-turbo")

# Prompts diferentes para cada ramo
prompt_1 = ChatPromptTemplate.from_template("Resuma este texto em uma frase: {texto}")
prompt_2 = ChatPromptTemplate.from_template("Traduz este texto para inglês: {texto}")

# Cadeias para cada ramo
chain_1 = prompt_1 | model | StrOutputParser()
chain_2 = prompt_2 | model | StrOutputParser()

# Executando em paralelo
parallel_chain = RunnableParallel(resumo=chain_1, traducao=chain_2)

# Input
texto = "O desenvolvimento de software é uma atividade complexa que requer planejamento e execução cuidadosos."

# Invocando
resultado = parallel_chain.invoke({"texto": texto})

print("Resumo:", resultado["resumo"])
print("Tradução:", resultado["traducao"])
```

---

```markdown
# Comentários em Arquivos LCEL

## Introdução
Adicionar comentários claros e objetivos em todos os arquivos LCEL para facilitar manutenção e colaboração.

---

## Diretrizes para Comentários

### 1. **Comentários de Arquivo**
- **Topo do arquivo**: Adicionar bloco de comentário com:
  - Propósito do pipeline.
  - Versão ou data de criação.
  - Autor (opcional).

  ```python
  # ---
  # Pipeline LCEL: Processamento de Dados de Usuários
  # Versão: 1.0
  # Data: 2024-05-20
  # Autor: [SeuNome]
  # ---
  ```

### 2. **Comentários de Funções/Pipeline**
- **Docstring** (para funções/pipelines):
  - Descrição do que faz.
  - Parâmetros esperados (se aplicável).
  - Retorno esperado.

  ```python
  def processar_dados_usuario(dados: list) -> dict:
      """
      Processa dados brutos de usuários e retorna um dicionário estruturado.

      Args:
          dados (list): Lista de dicionários com campos 'id', 'nome', 'email'.

      Returns:
          dict: Dicionário com chaves 'usuarios' (lista processada) e 'status'.
      """
      # ... implementação ...
  ```

### 3. **Comentários de Código**
- **Lógica complexa**: Explicar *por que* algo está sendo feito, não *o que*.
- **Evitar comentários óbvios**:
  ```python
  # ERRADO: x = x + 1  # Incrementa x em 1
  # CERTO: x += 1  # Atualiza contador de tentativas
  ```

### 4. **Comentários em Expressões LCEL**
- **Pipeline principal**: Comentar cada etapa crítica.
  ```python
  pipeline = (
      # 1. Filtra usuários ativos
      dados | filter(lambda x: x["ativo"])
      # 2. Agrupa por departamento
      | group_by(lambda x: x["departamento"])
      # 3. Mapeia para formato de saída
      | map(lambda g: {
          "departamento": g[0],
          "quantidade": len(g[1])
      })
  )
  ```

### 5. **Comentários de Configuração**
- **Variáveis de ambiente/parâmetros**:
  ```python
  # Configuração: Limite de requisições por minuto
  MAX_REQ_PER_MIN = 100  # Ajustado conforme política da API externa
  ```

---

## Exemplos Práticos

### Exemplo 1: Pipeline Completo
```python
# ---
# Pipeline: Extração de Dados de Vendas
# Responsável: Equipe de BI
# ---

from langchain_core.runnables import RunnablePassthrough

def criar_pipeline_vendas(dados_vendas):
    """
    Pipeline LCEL para processar dados de vendas.
    Saída: Dicionário com vendas por mês e produto.
    """
    return (
        # Etapa 1: Normalização de dados
        RunnablePassthrough.assign(
            mes=lambda x: x["data"].strftime("%Y-%m")
        )
        # Etapa 2: Agrupamento
        | RunnablePassthrough.assign(
            total_vendido=lambda x: x.groupby(["mes", "produto"])["valor"].sum()
        )
        # Etapa 3: Formatação final
        | lambda x: x.reset_index().to_dict("records")
    )
```

### Exemplo 2: Componente Personalizado
```python
class ValidadorEmail:
    """
    Componente LCEL para validar endereços de email.
    Usa regex para verificar formato padrão.
    """

    def __init__(self):
        import re
        self.padrao = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

    def validate(self, email: str) -> str:
        """Retorna email se válido, senão levanta ValueError."""
        if not self.padrao.match(email):
            raise ValueError(f"Email inválido: {email}")
        return email

# Uso no pipeline:
# ... | ValidadorEmail() | ...
```

---

## Ferramentas Recomendadas
- **VS Code**: Extensão "Python Docstring Generator" para criar docstrings automaticamente.
- **Pylint/Mypy**: Para detectar falta
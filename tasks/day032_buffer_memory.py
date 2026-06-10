```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# Inicializar o modelo de linguagem (substitua pela sua chave ou configuração)
llm = OpenAI(api_key="SUA_CHAVE_API_AQUI")

# Criar memória com histórico completo
memory = ConversationBufferMemory()

# Criar cadeia de conversação com a memória
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # Exibe logs detalhados
)

# Exemplo de uso
print("Iniciando conversação. Digite 'sair' para encerrar.")
while True:
    user_input = input("Você: ")
    if user_input.lower() == 'sair':
        break

    # Processar entrada e gerar resposta
    response = conversation.predict(input=user_input)
    print("Assistente:", response)

# Exibir histórico completo
print("\nHistórico completo da conversação:")
print(memory.buffer)
```

---

```markdown
# Comentários Detalhados nos Arquivos de Memória

## Introdução
Arquivos de memória em LangChain podem se beneficiar de comentários detalhados para facilitar manutenção, colaboração e depuração. Este guia aborda boas práticas para documentar arquivos de memória.

---

## Estrutura Básica de Comentários

### 1. Cabeçalho do Arquivo
```python
"""
Arquivo: memory_user_profiles.py
Descrição: Gerencia perfis de usuários em sessões de conversação.
Autor: [Seu Nome]
Data de Criação: DD/MM/AAAA
Versão: 1.0
Dependências:
    - langchain.memory
    - pydantic (>=2.0)
"""

from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel
```

### 2. Comentários em Classes e Funções
```python
class UserProfileMemory:
    """
    Gerencia o histórico de interações de um usuário específico.

    Atributos:
        memory (ConversationBufferMemory): Instância de memória para armazenar conversas.
        user_id (str): Identificador único do usuário.
    """

    def __init__(self, user_id: str):
        """
        Inicializa a memória do perfil do usuário.

        Args:
            user_id (str): ID único do usuário para indexação.
        """
        self.memory = ConversationBufferMemory(return_messages=True)
        self.user_id = user_id
```

### 3. Comentários em Métodos
```python
def save_interaction(self, message: str, response: str) -> None:
    """
    Salva uma interação usuário-assistente no histórico.

    Processo:
        1. Adiciona a mensagem do usuário ao buffer.
        2. Registra a resposta do assistente.
        3. Persiste automaticamente em armazenamento externo (se configurado).

    Args:
        message (str): Mensagem enviada pelo usuário.
        response (str): Resposta gerada pelo assistente.

    Exemplo:
        >>> memory.save_interaction("Qual é o clima hoje?", "Hoje está ensolarado.")
    """
    self.memory.chat_memory.add_user_message(message)
    self.memory.chat_memory.add_ai_message(response)
```

---

## Comentários Específicos para LangChain

### 1. Configurações de Memória
```python
def configure_memory(
    memory_type: str = "conversation_buffer",
    max_tokens: int = 1000,
    return_messages: bool = True
) -> ConversationBufferMemory:
    """
    Configura uma instância de memória com parâmetros otimizados.

    Parâmetros LangChain:
        - memory_type: Tipo de memória (ex: "conversation_buffer", "vector").
        - max_tokens: Limite de tokens para armazenamento.
        - return_messages: Se True, retorna mensagens formatadas como dicionários.

    Retorno:
        Instância configurada de ConversationBufferMemory.

    Notas:
        - Para memória vetorial, usar `VectorStoreRetrieverMemory`.
        - max_tokens afeta diretamente o custo de tokenização.
    """
    if memory_type == "conversation_buffer":
        return ConversationBufferMemory(
            max_tokens=max_tokens,
            return_messages=return_messages
        )
```

### 2. Persistência de Memória
```python
def save_memory_to_disk(
    memory: ConversationBufferMemory,
    file_path: str = "./memory/user_memory.json"
) -> None:
    """
    Serializa e salva a memória em disco no formato JSON.

    Formato de Saída:
        {
            "user_id": "123",
            "history": [
                {"role": "user", "content": "Olá"},
                {"role": "ai", "content": "Oi!"}
            ]
        }

    Args:
        memory (ConversationBufferMemory): Instância de memória a ser salva.
        file_path (str): Caminho para o arquivo de saída.

    Exceções:
        - ValueError: Se o formato de saída for inválido.
        - IOError: Se não houver permissão de escrita.
    """
    data = {
        "user_id": memory.user_id,
        "history": memory.chat_memory.messages
    }
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
```

---

## Boas Práticas

1. **Comentários de Evolução**:
   - Marque mudanças significativas com `@deprecated` ou `TODO`:
     ```python
     # TODO: Implementar compressão de histórico para reduzir custos de token
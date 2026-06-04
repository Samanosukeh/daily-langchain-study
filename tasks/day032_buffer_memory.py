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
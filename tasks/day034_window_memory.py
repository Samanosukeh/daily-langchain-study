```python
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# Inicializa o modelo de linguagem (substitua pela sua chave API ou modelo local)
llm = OpenAI(api_key="sua-chave-api")

# Configura a memória com janela de N mensagens (ex: 3 últimas mensagens)
memory = ConversationBufferWindowMemory(
    k=3,  # Tamanho da janela (quantas mensagens guardar)
    return_messages=True  # Retorna mensagens como lista de dicionários
)

# Cria a cadeia de conversação com a memória
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # Exibe logs para depuração
)

# Exemplo de uso
print("Início da conversa:")
print(conversation.predict(input="Olá, como você está?"))

print("\nResposta do modelo:")
print(conversation.predict(input="Qual é o seu nome?"))

print("\nResposta do modelo:")
print(conversation.predict(input="Quantos anos você tem?"))

print("\nResposta do modelo (deve lembrar apenas das 3 últimas mensagens):")
print(conversation.predict(input="Por que você não responde direito?"))
```
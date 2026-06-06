```python
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

# Inicializa o modelo (substitua pela sua chave)
llm = OpenAI(openai_api_key="sua-chave-api")

# Cria a memória de conversação
memory = ConversationBufferMemory()

# Cria a cadeia com memória
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# Exemplo de interação
print(conversation.run("Olá, como você está?"))
print(conversation.run("Qual é o meu nome?"))  # Não lembra ainda
print(conversation.run("Meu nome é João."))
print(conversation.run("Qual é o meu nome agora?"))  # Agora lembra
```
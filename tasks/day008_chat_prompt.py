```python
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Definindo mensagens do sistema e do usuário
system_template = "Você é um assistente útil que traduz {input_language} para {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

# Criando o ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([
    system_message_prompt,
    human_message_prompt
])

# Exemplo de uso
input_language = "inglês"
output_language = "português"
text = "Hello, how are you?"

# Formatando o prompt
formatted_messages = chat_prompt.format_messages(
    input_language=input_language,
    output_language=output_language,
    text=text
)

print("Mensagens formatadas:")
for message in formatted_messages:
    print(f"{message.type}: {message.content}")
```
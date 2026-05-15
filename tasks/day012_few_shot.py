```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.prompts.example_selector import FixedExampleSelector

# Exemplos fixos para FewShotPromptTemplate
examples = [
    {
        "task": "Traduzir a frase para inglês",
        "input": "Bom dia, como você está?",
        "output": "Good morning, how are you?"
    },
    {
        "task": "Traduzir a frase para inglês",
        "input": "Eu gosto de programar em Python",
        "output": "I like programming in Python"
    },
    {
        "task": "Traduzir a frase para inglês",
        "input": "Qual é a previsão do tempo para hoje?",
        "output": "What's the weather forecast for today?"
    }
]

# Template para os exemplos
example_prompt = PromptTemplate(
    input_variables=["task", "input", "output"],
    template="Task: {task}\nInput: {input}\nOutput: {output}"
)

# Selecionador de exemplos fixos
example_selector = FixedExampleSelector(examples=examples)

# FewShotPromptTemplate com os exemplos fixos
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Resolva as tarefas de tradução conforme os exemplos abaixo:\n\n",
    suffix="\nTask: {task}\nInput: {input}\nOutput:",
    input_variables=["task", "input"]
)

# Exemplo de uso
task = "Traduzir a frase para inglês"
input_phrase = "Até logo!"

prompt = few_shot_prompt.format(task=task, input=input_phrase)
print(prompt)
```
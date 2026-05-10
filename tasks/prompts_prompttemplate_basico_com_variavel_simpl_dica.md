```markdown
# Dicas Rápidas: `PromptTemplate` Básico com Variáveis

## 1. Instalação
```bash
pip install langchain
```

## 2. Importação
```python
from langchain.prompts import PromptTemplate
```

## 3. Template Simples
```python
template = "Olá, {nome}! Você tem {idade} anos."
prompt = PromptTemplate.from_template(template)
```

## 4. Formatação Dinâmica
```python
prompt.format(nome="João", idade=30)
# Saída: "Olá, João! Você tem 30 anos."
```

## 5. Variáveis Múltiplas
```python
template = "Crie um resumo de {livro} em {palavras} palavras."
prompt = PromptTemplate(template=template, input_variables=["livro", "palavras"])
```

## 6. Validação de Variáveis
```python
try:
    prompt.format(livro="1984")  # Erro: 'palavras' obrigatório
except ValueError as e:
    print(e)
```

## 7. Partialização (Valores Pré-definidos)
```python
prompt = PromptTemplate(
    template="Traduza '{texto}' para {idioma}.",
    input_variables=["texto"]
).partial(idioma="espanhol")
prompt.format(texto="Hello")
# Saída: "Traduza 'Hello' para espanhol."
```

## 8. Comentários no Template
```python
template = """# Comentário: Este é um template para perguntas
Pergunta: {pergunta}
Resposta:"""
```

## 9. Salvando/Recarregando
```python
prompt.save("template.json")  # Salva
PromptTemplate.from_file("template.json")  # Recarrega
```

## 10. Uso com Modelos
```python
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate.from_template("Diga-me um fato sobre {assunto}.")
chain = prompt | llm
print(chain.invoke({"assunto": "Python"}))
```
```
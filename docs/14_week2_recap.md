```markdown
# **Resumo da Semana 2: PromptTemplates**
**Tópico:** `prompts` | **Arquivo:** `docs/prompt_templates.md`

---

## **1. Conceito de PromptTemplates**
- **Definição:** Estrutura para padronizar a criação de *prompts* em aplicações LLM.
- **Objetivo:** Facilitar a reutilização, manutenção e dinamicidade dos inputs enviados ao modelo.
- **Base:** Herança de classes do LangChain (`BasePromptTemplate`).

---

## **2. Tipos de PromptTemplates**
### **2.1. `PromptTemplate`**
- **Uso:** Prompts estáticos ou com variáveis dinâmicas.
- **Exemplo:**
  ```python
  from langchain import PromptTemplate

  template = "Traduza o texto a seguir para {target_language}: {text}"
  prompt = PromptTemplate.from_template(template)
  formatted_prompt = prompt.format(target_language="francês", text="Olá mundo")
  ```
  **Saída:**
  ```text
  "Traduza o texto a seguir para francês: Olá mundo"
  ```

### **2.2. `FewShotPromptTemplate`**
- **Uso:** Prompts com exemplos (*few-shot learning*).
- **Componentes:**
  - `examples`: Lista de dicionários com `input`/`output`.
  - `example_prompt`: `PromptTemplate` para formatar cada exemplo.
- **Exemplo:**
  ```python
  from langchain import FewShotPromptTemplate, PromptTemplate

  examples = [
      {"input": "cachorro", "output": "animal"},
      {"input": "carro", "output": "veículo"}
  ]
  example_prompt = PromptTemplate(
      input_variables=["input", "output"],
      template="Entrada: {input}\nSaída: {output}"
  )
  few_shot_prompt = FewShotPromptTemplate(
      examples=examples,
      example_prompt=example_prompt,
      prefix="Classifique os seguintes termos:",
      suffix="Termo: {input_term}\nSaída:",
      input_variables=["input_term"]
  )
  print(few_shot_prompt.format(input_term="gato"))
  ```
  **Saída:**
  ```text
  Classifique os seguintes termos:
  Entrada: cachorro
  Saída: animal
  Entrada: carro
  Saída: veículo
  Termo: gato
  Saída:
  ```

### **2.3. `StringPromptTemplate` (Customizável)**
- **Uso:** Extensão para prompts personalizados.
- **Exemplo:**
  ```python
  from langchain.prompts import StringPromptTemplate
  from pydantic import BaseModel, validator

  class CustomPrompt(StringPromptTemplate, BaseModel):
      @validator("input_variables")
      def validate_input_variables(cls, v):
          if len(v) != 1 or "text" not in v:
              raise ValueError("Deve conter apenas 'text' como variável.")
          return v

      def format(self, **kwargs) -> str:
          return f"Resuma o seguinte texto em uma linha: {kwargs['text']}"

  prompt = CustomPrompt(input_variables=["text"])
  print(prompt.format(text="LangChain é uma biblioteca incrível."))
  ```
  **Saída:**
  ```text
  Resuma o seguinte texto em uma linha: LangChain é uma biblioteca incrível.
  ```

---

## **3. Boas Práticas**
1. **Variáveis Dinâmicas:**
   - Use `input_variables` para validar variáveis obrigatórias.
   - Exemplo:
     ```python
     template = PromptTemplate(
         input_variables=["adjective", "content"],
         template="Escreva um texto {adjective} sobre: {content}"
     )
     ```

2. **Prefixo/ Sufixo:**
   - Adicione contexto com `prefix` e `suffix`:
     ```python
     few_shot_prompt = FewShotPromptTemplate(
         prefix="Exemplos de tradução:",
         suffix="Traduza: {text}",
         ...
     )
     ```

3. **Validação:**
   - Use `pydantic` para garantir integridade dos dados:
     ```python
     from pydantic import BaseModel, validator

     class ValidatedPrompt(PromptTemplate, BaseModel):
         @validator("input_variables")
         def check_vars(cls, v):
             if "required_var" not in v:
                 raise ValueError("Variável 'required_var' obrigatória.")
             return v
     ```

---

## **4. Integração com LLMs**
-
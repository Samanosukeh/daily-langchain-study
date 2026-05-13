```python
from langchain.prompts import PromptTemplate

# Criando um PromptTemplate com uma variável simples
template = PromptTemplate.from_template(
    "Olá, {nome}! Como posso te ajudar hoje?"
)

# Exemplo de uso
nome_usuario = "João"
prompt_formatado = template.format(nome=nome_usuario)

print(prompt_formatado)
# Saída: Olá, João! Como posso te ajudar hoje?
```

---

```markdown
# Comentários nos Arquivos de Prompt

## Introdução
Em arquivos de prompt, comentários são essenciais para documentar intenções, exemplos e metadados sem afetar a execução. LangChain suporta comentários em diferentes formatos de arquivos de prompt.

---

## Sintaxe Básica

### Comentários em YAML
```yaml
# Comentário de linha em YAML
prompt: "Resuma este texto em 3 linhas."
# Autor: Dev Team
# Versão: 1.0
```

### Comentários em JSON
```json
{
  "prompt": "Analise o sentimento deste texto.",
  // Comentário em linha (não padrão JSON, mas suportado por algumas implementações)
  "metadata": {
    "author": "AI Team",
    "tags": ["análise", "sentimento"]
  }
}
```

### Comentários em TXT
```txt
# Comentário de linha em arquivos .txt
> Exemplo de prompt:
"Classifique este texto como positivo, negativo ou neutro."
# Observação: Usar para análise de reviews.
```

---

## Boas Práticas

1. **Mantenha comentários relevantes**:
   ```yaml
   # ERRADO: Comentário óbvio que não agrega valor
   # Define o campo 'prompt'
   prompt: "..."  # ERRADO: Comentário inline desnecessário
   ```

2. **Documente parâmetros**:
   ```yaml
   prompt: "Traduza para {lingua}."
   # Parâmetros:
   # - lingua: Código ISO (ex: 'pt', 'en')
   ```

3. **Versionamento**:
   ```yaml
   prompt: "Identifique entidades no texto."
   # Histórico:
   # v1.0 - Versão inicial
   # v1.1 - Adicionado suporte a entidades numéricas
   ```

4. **Exemplos no prompt**:
   ```yaml
   prompt: |
     Classifique o texto como:
     - "Positivo" se conter palavras como "ótimo", "bom".
     - "Negativo" se conter palavras como "ruim", "péssimo".
     - "Neutro" caso contrário.

     Exemplo:
     Texto: "O produto é bom, mas o atendimento foi péssimo."
     Classificação: "Negativo"
   ```

---

## Exemplo Completo (YAML)
```yaml
# Arquivo: templates/analise_sentimento.yaml
version: 1.2
author: "Equipe de NLP"
last_updated: "2024-02-20"

prompt: |
  Analise o sentimento do texto a seguir e classifique como:
  - "Positivo" (emoções agradáveis)
  - "Negativo" (emoções desagradáveis)
  - "Neutro" (sem emoção clara)

  Exemplo de uso:
  ---
  Texto: "Adorei o novo recurso, funciona perfeitamente!"
  Sentimento: "Positivo"
  ---

  Texto: "O sistema travou três vezes hoje."
  Sentimento: "Negativo"
  ---

# Parâmetros esperados:
# - texto: String com o conteúdo a ser analisado
```

---

## Ferramentas e Bibliotecas
- **LangChain PromptTemplate**: Ignora comentários em YAML/JSON automaticamente.
- **Hugging Face Prompt Files**: Suporta comentários em arquivos `.txt` com `#`.
- **Custom Parsers**: Implemente filtros para extrair metadados de comentários.

---

## Erros Comuns
1. **Comentários dentro de strings**:
   ```yaml
   # ERRADO: Comentário quebrando a sintaxe
   prompt: "Este é um # comentário dentro da string"
   ```

2. **Formatação inconsistente**:
   ```yaml
   # ERRADO: Mistura de estilos
   prompt: "..." # Comentário inline
   # Comentário de bloco
   ```

3. **Comentários em arquivos binários**: Não são suportados. Use arquivos de texto puro.
```
```markdown
# Human-in-the-loop: Pausar Grafo para Aprovação

## Visão Geral
Implementação de **human-in-the-loop** no LangGraph para pausar a execução do grafo e aguardar aprovação humana antes de prosseguir.

---

## Conceitos Chave
- **Pausa Condicional**: O grafo interrompe a execução em um nó específico.
- **Aprovação Externa**: Um humano valida ou rejeita a saída do nó pausado.
- **Reativação**: O grafo retoma a execução com base na decisão humana.

---

## Implementação

### 1. Definir Nó de Aprovação
Crie um nó que pause a execução e aguarde entrada humana.

```python
from langgraph.graph import Graph
from langgraph.prebuilt import ToolNode
from typing import Annotated
from typing_extensions import TypedDict

class State(TypedDict):
    input: str
    approved: bool
    feedback: str

def approval_node(state: State) -> State:
    """Nó que pausa o grafo para aprovação humana."""
    print(f"🔍 Entrada para aprovação: {state['input']}")
    print("Aguardando aprovação humana... (Digite 'aprovar' ou 'rejeitar')")
    while True:
        resposta = input("> ").strip().lower()
        if resposta in ("aprovar", "rejeitar"):
            return {"approved": resposta == "aprovar", "feedback": resposta}
        print("Resposta inválida. Digite 'aprovar' ou 'rejeitar'.")
```

---

### 2. Configurar Grafo com Condicional
Use `conditional_edge` para direcionar o fluxo com base na aprovação.

```python
workflow = Graph()

# Adiciona nós ao grafo
workflow.add_node("processamento", lambda state: {"input": f"Processado: {state['input']}"})
workflow.add_node("aprovação", approval_node)
workflow.add_node("feedback", lambda state: {"output": f"Resultado: {'Aprovado' if state['approved'] else 'Rejeitado'}"})

# Define edges
workflow.add_edge("processamento", "aprovação")

# Condicional: Aprovação ou Rejeição
workflow.add_conditional_edges(
    "aprovação",
    lambda state: "feedback" if state["approved"] else "fim",
    {
        "feedback": "feedback",  # Aprovado: continua
        "fim": END,              # Rejeitado: termina
    }
)

# Ponto de entrada
workflow.set_entry_point("processamento")
app = workflow.compile()
```

---

### 3. Executar o Grafo
Inicie o grafo e interaja com a pausa de aprovação.

```python
if __name__ == "__main__":
    input_usuario = input("Digite o texto a ser processado: ")
    result = app.invoke({"input": input_usuario})
    print(result)
```

---

## Fluxo de Execução
1. **Entrada**: Usuário fornece um texto.
2. **Processamento**: Nó `processamento` gera uma saída intermediária.
3. **Pausa**: Nó `aprovação` aguarda entrada humana.
4. **Decisão**:
   - Se **aprovado**, prossegue para `feedback`.
   - Se **rejeitado**, termina o grafo.
5. **Saída**: Exibe o resultado final.

---

## Personalização
- **Feedback Detalhado**: Adicione campos no `State` para justificativas humanas.
- **Timeout**: Implemente um limite de tempo para a aprovação.
- **Integração com Ferramentas**: Use `ToolNode` para validações automáticas pré-aprovação.

---

## Exemplo de Saída
```plaintext
Digite o texto a ser processado: Analisar este relatório.

🔍 Entrada para aprovação: Processado: Analisar este relatório.
Aguardando aprovação humana... (Digite 'aprovar' ou 'rejeitar')
> aprovar

{'output': 'Resultado: Aprovado'}
```

---

## Boas Práticas
- **Clareza**: Instruções explícitas para o usuário interagir.
- **Logs**: Registre decisões humanas para auditoria.
- **Tratamento de Erros**: Valide respostas inesperadas no nó de aprovação.
```
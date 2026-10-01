```python
from langchain_core.graphs import Graph

# Definindo nós
nodes = ["start", "process_data", "validate", "end_success", "end_error"]

# Definindo edges condicionais
edges = [
    ("start", "process_data"),
    ("process_data", "validate"),
    ("validate", "end_success", lambda x: x["is_valid"]),
    ("validate", "end_error", lambda x: not x["is_valid"]),
]

# Criando o grafo
graph = Graph(nodes=nodes, edges=edges)

# Executando o fluxo
input_data = {"is_valid": True}  # Teste com True/False
current_node = "start"

while current_node != "end_success" and current_node != "end_error":
    print(f"Nó atual: {current_node}")
    current_node = graph.next_node(current_node, input_data)

print(f"Fluxo finalizado no nó: {current_node}")
```
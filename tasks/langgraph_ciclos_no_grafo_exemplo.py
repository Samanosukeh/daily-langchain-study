```python
from typing import List, Dict, Tuple

def detect_cycle(graph: Dict[int, List[int]]) -> bool:
    """
    Detecta ciclos em um grafo direcionado usando DFS.
    Retorna True se houver ciclo, False caso contrário.
    """
    visited = set()
    recursion_stack = set()

    def dfs(node: int) -> bool:
        if node in recursion_stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        recursion_stack.add(node)

        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True

        recursion_stack.remove(node)
        return False

    for node in graph:
        if dfs(node):
            return True

    return False

# Exemplo de uso
grafo_com_ciclo = {
    1: [2],
    2: [3],
    3: [1]  # Ciclo: 1 -> 2 -> 3 -> 1
}

grafo_sem_ciclo = {
    1: [2],
    2: [3],
    3: []
}

print(detect_cycle(grafo_com_ciclo))  # Output: True
print(detect_cycle(grafo_sem_ciclo))  # Output: False
```
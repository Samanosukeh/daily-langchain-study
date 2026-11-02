```python
from mcstatus import JavaServer

def ping_servidor_minecraft(ip: str, porta: int = 25565):
    try:
        server = JavaServer.lookup((ip, porta))
        status = server.status()
        print(f"Jogadores online: {status.players.online}")
        print(f"Versão: {status.version.name}")
        print(f"Latência: {status.latency}ms")
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    ip_servidor = "localhost"  # Substitua pelo IP do servidor
    ping_servidor_minecraft(ip_servidor)
```
import subprocess
import platform

def check_online_sync(ip: str) -> bool:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout.lower()

        if platform.system().lower() == "windows":
            return f"resposta de {ip}" in output and "inacessível" not in output
        else:
            return "1 received" in output or "1 packets received" in output
    except Exception as e:
        print(f"Erro ao tentar pingar {ip}: {e}")
        return False

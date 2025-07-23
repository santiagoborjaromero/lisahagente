import subprocess
import requests
import json
import sys
import time

API_URL = "https://localhostr/api/recibir-resultados"
AUTH_TOKEN = "TuTokenSeguro"

def ejecutar_comando(comando):
    # print("[*] Ejecutando comando", comando)
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30  # segundos
        )
        # print("[=] Resultado", resultado)
        return {
            "stdout": resultado.stdout,
            "stderr": resultado.stderr,
            "returncode": resultado.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

def enviar_resultado(comando, resultado):
    payload = {
        "comando": comando,
        "resultado": resultado
    }
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        requests.post(API_URL, data=json.dumps(payload), headers=headers)
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el resultado: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 ejecutor.py 'comando_a_ejecutar'")
        sys.exit(1)

    comando = sys.argv[1]
    print(f"Ejecutando: {comando}")
    resultado = ejecutar_comando(comando)
    print(resultado)
    # print("Resultado:", resultado)
    # enviar_resultado(comando, resultado)
import subprocess
import requests
import json
import sys
import time

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

def enviar_resultado(resultado, token):
        # print("**************** PARAMS *******************")
        # print(resultado)
        print("**************** ENVIANDO *******************")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            respuesta = requests.post("http://172.20.0.6:5000/api/v1/savecmd/", json=resultado, headers=headers)
            print(respuesta)
        except Exception as e:
            print(f"[ERROR] No se pudo enviar el resultado: {e}")
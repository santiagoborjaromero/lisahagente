import subprocess
import requests
import json
import sys
import time
import base64
import configparser
import os

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
  config = configparser.ConfigParser()
  current_directory = os.getcwd()

  file_ini = f"{current_directory}/sentinel.ini"
  endpoint = ""

  if os.path.exists(file_ini):
    config.read(file_ini)
    endpoint = config.get("API", "endpoint")
    print(endpoint)
  else:
    print("The file does not exist.")
    return

  print("**************** ENVIANDO *******************")
  headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json"
  }

  try:
      respuesta = requests.post(f"{endpoint}/api/v1/savecmd/", json=resultado, headers=headers)
      print(respuesta)
  except Exception as e:
      print(f"[ERROR] No se pudo enviar el resultado: {e}")
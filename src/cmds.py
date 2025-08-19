import subprocess
import requests
import json
import sys
import time
import base64
import configparser
import os
from datetime import datetime
from src.entities.hcommand import HCommand
from src.database import conn 

def ejecutar_comando(comando, usuario="soft8"):
    # newcomand = f"sudo -u {usuario} {comando}"
    newcomand = comando
    # print("comando", newcomand)
    try:
        resultado = subprocess.run(
            newcomand,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            # check=True,
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



def enviar_resultado(ddata:HCommand, token):
  sudo setenforce 0

def guardar_postgresql(ddata:HCommand):
  documento = dict(ddata)

  accion = documento["action"]
  identificador = documento["identificador"]
  # print(identificador)
  data = documento["data"]
  idcliente = identificador["idcliente"]
  idusuario = identificador["idusuario"]
  idservidor = identificador["idservidor"]
  idoperacion = identificador["id"]

  conn.autocommit = True
  cur = conn.cursor()

  for dt in data:
    idcola_comando = dt["id"]
    comando = dt["cmd"]
    respuesta = dt["respuesta"]
    now = datetime.now()
    fecha = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
      rs = cur.execute("""INSERT INTO historico_comandos (idcliente,idusuario,idservidor,idoperacion,idcola_comando,fecha,comando,respuesta,accion) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""", (idcliente, idusuario, idservidor, idoperacion, idcola_comando, fecha, comando, respuesta, accion, ))
      conn.commit()
    except Exception as err:
      print(err)
  
  # conn.close()


def traer_logs(idcliente, idservidor, rango = ""):
  conn.autocommit = True
  status = False
  data = []
  # data = conn.query(HCommand).filter(HCommand.idcliente == idcliente, HCommand.idservidor == idservidor).all()
  cursor = conn.cursor()
  try:
    cursor.execute(f"SELECT * FROM historico_comandos WHERE idcliente=%s AND idservidor=%s", (idcliente, idservidor))
    data = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    status = True
    conn.commit()
  except Exception as err:
    print(err)
  
  # cursor.close()
  # conn.close()
  return {
    "status": status,
    "data": data,
    "colnames": colnames
  }
  


def saveLog(data, level="INFO"):
  config = configparser.ConfigParser()
  current_directory = os.getcwd()
  file_ini = f"{current_directory}/sentinel.ini"

  path_folder_log = ""

  if os.path.exists(file_ini):
    config.read(file_ini)
    path_folder_log = config.get("APP", "logs")
    # print(path_folder_log)
  else:
    print("The file does not exist.")
    return
  

  fecha_file =  datetime.now().strftime("%Y%m%d")
  fecha =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  file = f"{path_folder_log}/lisah-sentinel-{fecha_file}.log"


  if not os.path.exists(path_folder_log):
    os.makedirs(path_folder_log)

  txt = f"{fecha} [{level}] {data} \n"

  file = open(file, "a")
  file.write(txt)
  file.close()

  
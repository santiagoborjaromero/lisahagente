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
# from src.mongodb import db
# from src.postgresql import conn

def dondeGuardaLogs():
  path_folder_log = "/var/log/sentinel"
  if not os.path.exists(path_folder_log):
     os.makedirs(path_folder_log)
  return path_folder_log

def ejecutar_comando(comando, usuario="soft8"):
  # newcomand = f"sudo -u {usuario} {comando}"
  newcomand = f"sudo {comando}"
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


#
# FILES
#
def saveData(fuente):
  path_folder_log = dondeGuardaLogs()

  fecha_file =  datetime.now().strftime("%Y%m%d")
  fecha =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  data = {
    "action": fuente["action"],
    "fecha": fecha,
    "id": fuente["identificador"]["id"],
    "idcliente": fuente["identificador"]["idcliente"],
    "idusuario": fuente["identificador"]["idusuario"],
    "idservidor": fuente["identificador"]["idservidor"],
    "usuario": fuente["identificador"]["usuario"],
    "data": fuente["data"]
  }

  file = f"{path_folder_log}/sentinel-{fecha_file}.lisah"

  if not os.path.exists(path_folder_log):
    os.makedirs(path_folder_log)

  data_str = json.dumps(data)
  data_string_bytes = data_str.encode("ascii")
  base64_bytes = base64.b64encode(data_string_bytes)
  dataB64 = base64_bytes.decode("ascii")

  file = open(file, "a")
  file.write( dataB64 + "\n")
  file.close()


def enviar_resultado(ddata, token):
  print("")


# def traer_logs(idcliente, idservidor, fecha, idusuario_select):

#   print(idcliente, idservidor, fecha, idusuario_select)

#   path_folder_log = dondeGuardaLogs()
#   fecha_file =  fecha.replace("-", "")
#   contenido = os.listdir(path_folder_log)

#   data = []
#   status = True
#   string_data = ""

#   try:
#     for fichero in contenido:
#       if os.path.isfile(os.path.join(path_folder_log, fichero)) and fichero.endswith('.lisah'):
#         if fecha_file in fichero:
#           print(f"Abriendo {fichero}")
#           with open(path_folder_log + "/" + fichero, 'r', encoding='utf-8') as archivo:
#             for linea in archivo:
#               content = json.loads(  base64.b64decode(linea) ) 
#               if idusuario_select != 0:
#                 if content["idusuario"] == idusuario_select:
#                   data.append( content )
#               else:
#                 data.append( content )

#   except Exception as err:
#     status = False
#     data = []

#   print(len(data))
#   return {"status": status, "data": data}


def traer_logs(idcliente, idservidor, fecha, idusuario):
  print(idcliente, idservidor, fecha, idusuario)

  fecha_file =  fecha.replace("-", "")
  path_folder_log = dondeGuardaLogs()
  contenido = os.listdir(path_folder_log)

  data = []
  datatemp = []
  status = True

  try:
    for fichero in contenido:
      if os.path.isfile(os.path.join(path_folder_log, fichero)) and fichero.endswith('.lisah'):
        if fecha_file in fichero:
          print(f"Abriendo {fichero}")
          with open(path_folder_log + "/" + fichero, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
              try:
                content = json.loads( base64.b64decode(linea) )
                if (idusuario == "0"):
                  data.append(content)  
                else:
                  if content["idusuario"] == int(idusuario):
                    data.append(content)  
              except Exception as err:
                status = False
                data = err
                print(f"Error traer log: {err}")
  except Exception as err:
    status = False
    data = err

  return {"status": status, "data": data}


def statsServer(idcliente, idservidor, idusuario, fecha):
  fecha_file =  fecha.replace("-", "")
  path_folder_log = dondeGuardaLogs()
  contenido = os.listdir(path_folder_log)

  data = []
  datatemp = []
  status = True

  count = 0
  total = 0

  try:
    for fichero in contenido:
      if os.path.isfile(os.path.join(path_folder_log, fichero)) and fichero.endswith('.lisah'):
        if fecha_file in fichero:
          print(f"Abriendo {fichero}")
          with open(path_folder_log + "/" + fichero, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
              total = total + 1
              content =  json.loads( base64.b64decode(linea) )
              if content["idusuario"] == idusuario:
                  count = count + 1
  except Exception as err:
    status = False
    count = 0
    total = 0

  return [count, total]


#
# MONGO
#

# def enviar_resultado(ddata, token):
#   documento = dict(ddata)

#   accion = documento["action"]
#   identificador = documento["identificador"]
#   data = documento["data"]
#   idcliente = identificador["idcliente"]
#   idusuario = identificador["idusuario"]
#   idservidor = identificador["idservidor"]
#   idoperacion = identificador["id"]

#   for d in data:
#       now = datetime.now()
#       fecha = now.strftime("%Y-%m-%d %H:%M:%S")
#       hcmd = HCommand(
#         idcliente = identificador["idcliente"],
#         idservidor = identificador["idusuario"],
#         idusuario = identificador["idservidor"],
#         idoperacion = identificador["id"],
#         idcola_comando = d["id"],
#         fecha = fecha,
#         comando = d["cmd"],
#         resultado = d["respuesta"],
#         accion = accion
#       )
#       try:
#           resp = db.historico_comandos.insert_one(dict(hcmd))
#           print("RESPUESTA", resp)
#       except Exception as err:
#           print("ERROR insert", err)

# async def traer_logs(idcliente, idservidor, rango = ""):
#   status = False
#   data = []
#   now = datetime.now()
#   # fecha = now.strftime("%Y-%m-%d %H:%M:%S")
#   fecha = now.strftime("%Y-%m-%d")

#   try:
#     filtro = {
#       "idcliente": idcliente,
#       "idservidor": idservidor,
#       'fecha': {
#         "$regex": f"^{fecha}",  # Empieza con "2025-08-19"
#         "$options": "i"  # Insensible a mayúsculas
#       }
#     }
#     print(filtro)
#     data = await db.historico_comandos.find(filtro).to_list(length=None)
#     # for item in data:
#     #   item["_id"] = str(item["_id"])
#     print(data)
#     status = True
#   except Exception as err:
#     print("ERROR GET", err)

#   return {
#     "status": status,
#     "data": data,
#   }







# def guardar_postgresql(ddata:HCommand):
#   documento = dict(ddata)

#   accion = documento["action"]
#   identificador = documento["identificador"]
#   # print(identificador)
#   data = documento["data"]
#   idcliente = identificador["idcliente"]
#   idusuario = identificador["idusuario"]
#   idservidor = identificador["idservidor"]
#   idoperacion = identificador["id"]

#   conn.autocommit = True
#   cur = conn.cursor()

#   for dt in data:
#     idcola_comando = dt["id"]
#     comando = dt["cmd"]
#     respuesta = dt["respuesta"]
#     now = datetime.now()
#     fecha = now.strftime("%Y-%m-%d %H:%M:%S")

#     try:
#       rs = cur.execute("""INSERT INTO historico_comandos (idcliente,idusuario,idservidor,idoperacion,idcola_comando,fecha,comando,respuesta,accion)
#       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""", (idcliente, idusuario, idservidor, idoperacion, idcola_comando, fecha, comando, respuesta, accion, ))
#       conn.commit()
#     except Exception as err:
#       print(err)

#   # conn.close()


# def traer_logs(idcliente, idservidor, rango = ""):
#   conn.autocommit = True
#   status = False
#   data = []
#   # data = conn.query(HCommand).filter(HCommand.idcliente == idcliente, HCommand.idservidor == idservidor).all()
#   cursor = conn.cursor()
#   try:
#     cursor.execute(f"SELECT * FROM historico_comandos WHERE idcliente=%s AND idservidor=%s", (idcliente, idservidor))
#     data = cursor.fetchall()
#     colnames = [desc[0] for desc in cursor.description]
#     status = True
#     conn.commit()
#   except Exception as err:
#     print(err)

#   # cursor.close()
#   # conn.close()
#   return {
#     "status": status,
#     "data": data,
#     "colnames": colnames
#   }



def saveLog(data, level="INFO", audit=False):
  path_folder_log = dondeGuardaLogs()

  fecha_file =  datetime.now().strftime("%Y%m%d")
  fecha =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  if (audit):
    ext = "audit"
  else:
    ext = "log"

  file = f"{path_folder_log}/lisah-sentinel-{fecha_file}.{ext}" 

  if not os.path.exists(path_folder_log):
    os.makedirs(path_folder_log)

  txt = f"{fecha} [{level}] {data} \n"

  file = open(file, "a")
  file.write(txt)
  file.close()


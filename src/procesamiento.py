import threading
from src.entities.request import Request, Data
from src.cmds import ejecutar_comando, enviar_resultado, saveLog, traer_logs, saveData, statsServer
from src.functions import encrypt, decrypt
from concurrent.futures import thread
import json
import threading
import asyncio
from datetime import datetime

class Procesamiento:

    async def clasificacion(info: Request, token:str):
        request = json.loads(info)
        # saveLog(json.dumps(request), "JSON")

        descrypt_token  = json.loads(decrypt(token))

        action          = request["action"]
        identificador   = request["identificador"]
        idtransaccion   = identificador["id"]
        idusuario       = identificador["idusuario"]
        idcliente       = identificador["idcliente"]
        idservidor      = identificador["idservidor"]
        usuario         = identificador["usuario"]

        d_idusuario     = descrypt_token["idusuario"]
        d_idcliente     = descrypt_token["idcliente"]

        if d_idusuario != idusuario or d_idcliente != idcliente:
            saveLog("ENTRADA NO AUTORIZADA", "AUTH")
            return request

        if (action == "comando"):
            data = request["data"]
            
            response = {
                "action": action,
                "identificador": identificador,
                "data": []
            }

            data_response = []

            for r in data:

                comando = r["cmd"]
                ref =  r["id"]

                resp = ejecutar_comando(comando, usuario)

                respuesta_original = ""

                if resp["stderr"] == "":
                    respuesta_original = resp["stdout"]
                    saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando} RESPONSE={respuesta_original}", "DEBUG")
                else:
                    respuesta_original = resp["stderr"]
                    saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando} RESPONSE={respuesta_original}", "ERROR")
                    print("ERROR", resp["stderr"])
                
                
                # print(comando)
                # print(respuesta_original)
                respuesta = encrypt(respuesta_original)
                # print(respuesta)

                response["data"].append({
                    "id": r["id"],
                    "cmd": encrypt(r["cmd"]),
                    "respuesta": respuesta,
                })

            # enviar_resultado(response,token)
            saveData(response)
            return response
        # elif (action == "lista_servicios"):

        #     cmd = '''
        #     {
        #         systemctl list-unit-files --type=service --no-legend | \
        #         awk '$1 ~ /\.service$/ && $1 !~ /@/  {print $1}' | \
        #         while read servicio; do
        #             descripcion=$(systemctl show -p Description --value "$servicio" 2>/dev/null | sed 's/,/;/g' || echo "Sin descripción")
        #             loaded=$(systemctl is-enabled "$servicio" 2>/dev/null || echo "disabled")
        #             active=$(systemctl is-active "$servicio" 2>/dev/null | awk '{print $1}' ||  echo "inactive")
        #             printf '%s,%s,%s,%s|' "$servicio" "$descripcion" "$loaded" "$active"
        #         done
        #     } 
        #     '''

        #     rsp = ejecutar_comando(cmd)
        #     if rsp["stderr"] == "":
        #         salida = rsp["stdout"].strip()
        #         servicios = [s for s in salida.split('|') if s.strip()]
        #         ac = ""
        #         for s in servicios:
        #             try:
        #                 servicio, descripcion, loaded, active = s.split(',', 3)
        #                 ac = ac + f"{servicio},{descripcion},{loaded},{active}|"
        #             except Exception as e:
        #                 saveLog(f"Error parseando: {s} -> {e}", "ERROR")
        #                 print(f"Error parseando: {s} -> {e}")
        #     else:
        #         respuesta_error = rsp["stderr"]
        #         saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando} RESPONSE={respuesta_error}", "ERROR")

        #     response = {
        #         "action": action,
        #         "identificador": identificador,
        #         "data":  [{
        #             "id": action,
        #             "cmd": "",
        #             "respuesta": encrypt(ac)
        #         }]  
        #     }
        #     saveData(response)
        #     return response
        elif (action == "stats"):
            comandos = [
                {"id": "disco", "cmd":" df -hT | grep -E 'ext4|xfs|btrfs' | awk '{print $3, $4, $5}'"},
                {"id": "cpu", "cmd":"cat /proc/loadavg | awk '{print $1, $2, $3}'"},
                {"id": "memoria", "cmd":"free -h | grep -E 'Mem' | awk '{print $2, $3, $4}'"},
                {"id": "uptime", "cmd":'sec=$(( $(date +%s) - $(date -d "$(ps -p 1 -o lstart=)" +%s) )); d=$((sec/86400)); h=$(( (sec%86400)/3600 )); m=$(( (sec%3600)/60 )); s=$((sec%60)); printf "%02d:%02d:%02d:%02d\n" $d $h $m $s'},
                {"id": "servicio_httpd", "cmd":"systemctl is-active httpd"},
                {"id": "servicio_ssh", "cmd":"systemctl is-active sshd"},
                {"id": "release", "cmd":"cat /etc/os-release"},
            ]

            response = {
                "action": request["action"],
                "identificador": request["identificador"],
                "data": []
            }

            for r in comandos:
                comando = r["cmd"]
                ref =  r["id"]

                resp = ejecutar_comando(comando)

                if resp["stderr"] == "":
                    respuesta = resp["stdout"]
                else:
                    respuesta = resp["stderr"]
                    saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando} RESPONSE={respuesta}", "ERROR")
                

                # print(respuesta)
                response["data"].append({
                    "id": r["id"],
                    "cmd": encrypt(r["cmd"]),
                    "respuesta": encrypt(respuesta),
                })

            # enviar_resultado(response, token)
            saveLog(json.dumps(response), "stats")
            saveData(response)
            return response
        elif (action == "logs"):
            # response = await traer_logs(idcliente, idservidor)
            fecha = identificador["fecha"]
            response = traer_logs(idcliente, idservidor, fecha)
            saveLog(json.dumps(response), "logs")
            saveData(response)
            return response 
        elif (action == "statserver"):
            fecha = identificador["fecha"]
            result = statsServer(idcliente, idservidor, idusuario, fecha)
            response = {
                "action": request["action"],
                "identificador": request["identificador"],
                "data": result,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            saveLog(json.dumps(response), "statserver")
            saveData(response)
            return response

        return response

        

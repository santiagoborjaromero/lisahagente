# from concurrent.futures import thread
import threading
# import subprocess
from src.entities.request import Request, Data
from src.cmds import ejecutar_comando
import json

class Procesamiento:
    def bloque(data):
        print(data)

    def clasificacion(info: Request):
        request = json.loads(info)

        if (request["action"] == "comando"):
            data = request["data"]
            
            response = {
                "action": request["action"],
                "identificador": request["identificador"],
                "data": []
            }
            print(response)

            data_response = []

            for r in data:
                resp = ejecutar_comando(r["cmd"])

                print(resp)

                respuesta = resp["stderr"]

                if resp["stderr"] == "":
                    respuesta = resp["stdout"]
                    # respuesta = string.replace("\n", "", respuesta)
                
                print("█", respuesta)

                response["data"].append({
                    "id": r["id"],
                    "cmd": r["cmd"],
                    "respuesta": respuesta,    
                })

                # data_response.append({
                #     id: r["id"],
                #     cmd: r["cmd"],
                #     respuesta: respuesta,
                # })
            
            # response["data"] = data_response
            return response
        elif (request["action"] == "stats"):
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
                "referencia": request["referencia"],
                "data": []
            }

            for r in comandos:
                respuesta = ejecutar_comando(r["cmd"])
                print(respuesta)
                response["data"].append({
                    "id": r["id"],
                    # "cmd": r["cmd"],
                    "respuesta": respuesta,    
                })


        return response


import threading
from src.entities.request import Request, Data
from src.cmds import ejecutar_comando, enviar_resultado, saveLog
from src.encrypt import encrypt
import json
from concurrent.futures import thread
import threading

class Procesamiento:

    def bloque(data):
        print(data)

    def clasificacion(info: Request, token:str):
        request = json.loads(info)
        saveLog(json.dumps(request), "JSON")

        action = request["action"]
        identificador = request["identificador"]
        idtransaccion = identificador["id"]
        idusuario = identificador["idusuario"]

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
                resp = ejecutar_comando(comando)

                respuesta_original = ""

                if resp["stderr"] == "":
                    respuesta_original = resp["stdout"]
                    saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando}", "INFO")
                else:
                    respuesta_original = resp["stderr"]
                    saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando} RESPONSE={respuesta_original}", "ERROR")
                
                
                try:
                    respuesta = respuesta_original.encode("ascii", "replace")
                    respuesta = respuesta.decode(encoding="utf-8", errors="ignore")
                except Exception as err:
                    print(err)
                    respuesta = respuesta_original

                response["data"].append({
                    "id": r["id"],
                    "cmd": encrypt(r["cmd"]),
                    "respuesta": encrypt(respuesta),
                })

            thread = threading.Thread(target=enviar_resultado, args=(response,token,))
            thread.start()
            
            return response
        elif (action == "lista_servicios"):

            cmd = '''
            {
                systemctl list-unit-files --type=service --no-legend | \
                awk '$1 ~ /\.service$/ && $1 !~ /@/  {print $1}' | \
                while read servicio; do
                    descripcion=$(systemctl show -p Description --value "$servicio" 2>/dev/null | sed 's/,/;/g' || echo "Sin descripción")
                    loaded=$(systemctl is-enabled "$servicio" 2>/dev/null || echo "disabled")
                    active=$(systemctl is-active "$servicio" 2>/dev/null | awk '{print $1}' ||  echo "inactive")
                    printf '%s,%s,%s,%s|' "$servicio" "$descripcion" "$loaded" "$active"
                done
            } 
            '''

            rsp = ejecutar_comando(cmd)

            salida = rsp["stdout"].strip()
            servicios = [s for s in salida.split('|') if s.strip()]
            ac = ""
            for s in servicios:
                try:
                    servicio, descripcion, loaded, active = s.split(',', 3)
                    ac = ac + f"{servicio},{descripcion},{loaded},{active}|"
                except Exception as e:
                    print(f"Error parseando: {s} -> {e}")

            saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF= CMD={cmd}", "INFO")

            response = {
                "action": action,
                "identificador": identificador,
                "data":  [{
                    "id": action,
                    "cmd": "",
                    "respuesta": encrypt(ac)
                }]  
            }
            
            return response
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
                    saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando}", "INFO")
                else:
                    respuesta = resp["stderr"]
                    saveLog(f"ID={idtransaccion} IDUSUARIO={idusuario} REF={ref} CMD={comando} RESPONSE={respuesta}", "ERROR")
                

                print(respuesta)
                response["data"].append({
                    "id": r["id"],
                    "cmd": encrypt(r["cmd"]),
                    "respuesta": encrypt(respuesta),
                })

        # enviar_resultado(response)
        return response

        

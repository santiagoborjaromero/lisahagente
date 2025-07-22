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
        return ""


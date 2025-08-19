import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import  datetime, timedelta, timezone
import json

def encrypt(plaintext):
    resultado_string_bytes = plaintext.encode("ascii")
    base64_bytes = base64.b64encode(resultado_string_bytes)
    resultadoB64 = base64_bytes.decode("ascii")
    return resultadoB64


def decrypt(data):
    passphrase = "7PToGGTJ71knRd86WF39wfj619qewnbZ"
    key = passphrase.encode('utf-8')[:32]
    iv = b'cAbBrz3Lzy4Ucwhx'

    try:
        cdata1 = base64.b64decode(data)
        cdata = base64.b64decode(cdata1)
        ciphertext = cdata

        if len(ciphertext) % AES.block_size != 0:
            raise ValueError("El texto cifrado no tiene tamaño múltiplo de 16 bytes")

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext_padded = cipher.decrypt(ciphertext)

        try:
            plaintext = unpad(plaintext_padded, AES.block_size).decode('utf-8')
        except (ValueError, TypeError):
            plaintext = plaintext_padded.decode('utf-8', errors='replace').rstrip('\x00').strip()

    except Exception as e:
        plaintext = f"Error al descifrar: {str(e)}"

    return plaintext

def validate_token(token):
    jwt = ""
    try:
        jwt = decrypt(token)
        message = jwt
        if "Error" in jwt:
            status = False 
        else:
            fecha =  datetime.now()
            fecha_utc5 = fecha + timedelta(hours=-5)

            status = True
            message = json.loads(jwt)
            fecha_caducidad = message["expire_date"]
            if fecha_caducidad >= fecha_utc5.strftime("%Y-%m-%d %H:%M:%S"):
                status = True
            else:
                status = False
                message = "Token Expirado"

        return {"status": status, "message": message}
    except Exception as ex:
        print("Error jwt", ex)
        return {"status": status, "message": ex}
    
    


    
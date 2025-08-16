import base64

def encrypt(plaintext):
    resultado_string_bytes = plaintext.encode("ascii")
    base64_bytes = base64.b64encode(resultado_string_bytes)
    resultadoB64 = base64_bytes.decode("ascii")
    return resultadoB64


    
import base64
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad

# passphrase = "7PToGGTJ71knRd86WF39wfj619qewnbZ"
# key = passphrase.encode('utf-8')[:32]
# iv = b'cAbBrz3Lzy4Ucwhx'

def encrypt(plaintext):
    resultado_string_bytes = plaintext.encode("ascii")
    base64_bytes = base64.b64encode(resultado_string_bytes)
    resultadoB64 = base64_bytes.decode("ascii")
    return resultadoB64


# def encrypt(plaintext):
#     try:
#         # Asegurarse de que el plaintext sea bytes
#         if isinstance(plaintext, str):
#             plaintext = plaintext.encode('utf-8')

#         # Aplicar padding PKCS7
#         padded_plaintext = pad(plaintext, AES.block_size)

#         # Crear cifrador AES en modo CBC
#         cipher = AES.new(key, AES.MODE_CBC, iv=iv)
#         ciphertext = cipher.encrypt(padded_plaintext)

#         # Codificar en Base64 dos veces
#         encoded = base64.b64encode(ciphertext)

#         # Devolver como string
#         return encoded.decode('utf-8')

#     except Exception as e:
#         return f"Error al cifrar: {str(e)}"

# def decrypt(data):
#     try:
#         cdata1 = base64.b64decode(data)
#         cdata = base64.b64decode(cdata1)
#         ciphertext = cdata

#         if len(ciphertext) % AES.block_size != 0:
#             raise ValueError("El texto cifrado no tiene tamaño múltiplo de 16 bytes")

#         cipher = AES.new(key, AES.MODE_CBC, iv=iv)
#         plaintext_padded = cipher.decrypt(ciphertext)

#         try:
#             plaintext = unpad(plaintext_padded, AES.block_size).decode('utf-8')
#         except (ValueError, TypeError):
#             plaintext = plaintext_padded.decode('utf-8', errors='replace').rstrip('\x00').strip()

#     except Exception as e:
#         plaintext = f"Error al descifrar: {str(e)}"

#     return plaintext
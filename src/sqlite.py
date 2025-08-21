import sqlite3

def createDatabase():
    now = datetime.now()
    nombre_archivo = now.strftime("lisah_%Y%m%d.db")
    conn = sqlite3.connect(nombre_archivo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            idhistorico_comando INTEGER PRIMARY KEY,
            idcliente INT,
            idservidor INT
            idusuario INT,
            idoperacion INT,
            referencia TEXT,
            fecha TEXT,
            accion TEXT,
            comando TEXT,
            respuesta TEXT,
        )
    ''')


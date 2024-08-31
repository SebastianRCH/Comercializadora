from db import conectar_db

def autenticar_usuario(username, password):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username=%s AND password=%s', (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None
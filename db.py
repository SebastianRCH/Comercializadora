import mysql.connector

def conectar_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",     
        password="",    
        database="python_dev",
        port=3306   
    )
    return conn

def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    conn.commit()
    conn.close()

def insertar_cliente_proveedor(nombre, apellido, documento_identidad, numero_telefonico, direccion, correo_electronico):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes_proveedores (nombre, apellido, documento_identidad, numero_telefonico, direccion, correo_electronico)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nombre, apellido, documento_identidad, numero_telefonico, direccion, correo_electronico))
    conn.commit()
    conn.close()

def obtener_clientes_proveedores():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes_proveedores')
    registros = cursor.fetchall()
    conn.close()
    return registros

def actualizar_cliente_proveedor(id_cliente, nombre, apellido, documento_identidad, numero_telefonico, direccion, correo_electronico):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes_proveedores
        SET nombre=%s, apellido=%s, documento_identidad=%s, numero_telefonico=%s, direccion=%s, correo_electronico=%s
        WHERE id=%s
    ''', (nombre, apellido, documento_identidad, numero_telefonico, direccion, correo_electronico, id_cliente))
    conn.commit()
    conn.close()

def eliminar_cliente_proveedor(id_cliente):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes_proveedores WHERE id=%s', (id_cliente,))
    conn.commit()
    conn.close()    
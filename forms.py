import tkinter as tk
from tkinter import ttk, messagebox
import random
from db import insertar_cliente_proveedor, obtener_clientes_proveedores, actualizar_cliente_proveedor, eliminar_cliente_proveedor

def centrar_ventana(ventana, ancho, alto):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def abrir_formulario_gerente(root):
    ventana = tk.Toplevel(root)
    ventana.title("Consultar Todos los Clientes")
    centrar_ventana(ventana, 800, 400) 

    columnas = ("ID", "Nombre", "Apellido", "Documento", "Teléfono", "Dirección", "Correo")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    registros = obtener_clientes_proveedores()

    for reg in registros:
        tree.insert("", tk.END, values=reg)
    
    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def abrir_formulario_administrador(root):
    ventana = tk.Toplevel(root)
    ventana.title("Editar Clientes/Proveedores")
    centrar_ventana(ventana, 800, 400)  

 
    columnas = ("ID", "Nombre", "Apellido", "Documento", "Teléfono", "Dirección", "Correo")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    

    registros = obtener_clientes_proveedores()
    

    for reg in registros:
        tree.insert("", tk.END, values=reg)
    
    tree.pack(fill=tk.BOTH, expand=True)


    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    

    frame_edicion = tk.Frame(ventana)
    frame_edicion.pack(fill=tk.X, pady=10)
    
    tk.Button(frame_edicion, text="Editar", command=lambda: editar_registro(tree)).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_edicion, text="Eliminar", command=lambda: eliminar_registro(tree)).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_edicion, text="Actualizar Lista", command=lambda: actualizar_lista(tree)).pack(side=tk.LEFT, padx=10)

def editar_registro(tree):

    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Selección Vacía", "Por favor, seleccione un registro para editar.")
        return
    

    item = tree.item(seleccion[0])
    valores = item['values']
    
    ventana_edicion = tk.Toplevel(tree)
    ventana_edicion.title("Editar Registro")
    centrar_ventana(ventana_edicion, 400, 300)


    labels = ["Nombre", "Apellido", "Documento de identidad o NIT", "Número telefónico", "Dirección", "Correo electrónico"]
    entries = {}
    
    for i, label in enumerate(labels, start=1):
        tk.Label(ventana_edicion, text=label).pack(anchor="w", padx=10)
        entry = tk.Entry(ventana_edicion, width=40)
        entry.pack(padx=10, pady=5)
        entry.insert(0, valores[i]) 
        entries[label] = entry


    def guardar_cambios():
        nombre = entries["Nombre"].get()
        apellido = entries["Apellido"].get()
        documento_identidad = entries["Documento de identidad o NIT"].get()
        numero_telefonico = entries["Número telefónico"].get()
        direccion = entries["Dirección"].get()
        correo_electronico = entries["Correo electrónico"].get()

        actualizar_cliente_proveedor(valores[0], nombre, apellido, documento_identidad, numero_telefonico, direccion, correo_electronico)
        
        messagebox.showinfo("Confirmación", f"Registro de {nombre} {apellido} actualizado correctamente.")
        ventana_edicion.destroy()
        actualizar_lista(tree)

    tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios).pack(pady=10)

def eliminar_registro(tree):

    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Selección Vacía", "Por favor, seleccione un registro para eliminar.")
        return
    
    confirmacion = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este registro?")
    if confirmacion:
        item = tree.item(seleccion[0])
        valores = item['values']
        eliminar_cliente_proveedor(valores[0])  
        messagebox.showinfo("Eliminación Exitosa", f"El registro ha sido eliminado.")
        actualizar_lista(tree)

def actualizar_lista(tree):

    for item in tree.get_children():
        tree.delete(item)
    

    registros = obtener_clientes_proveedores()
    for reg in registros:
        tree.insert("", tk.END, values=reg)

    def crear_cliente_proveedor():
        idx = combo_seleccion.current()
        if idx != -1:
            cliente_proveedor = registros[idx]
            tk.Label(ventana, text=f"Cliente/Proveedor creado: {cliente_proveedor[1]} {cliente_proveedor[2]}", fg="green").pack(pady=5)

    registros = obtener_clientes_proveedores()
    opciones = [f"{i + 1}. {reg[1]} {reg[2]}" for i, reg in enumerate(registros)]
    
    tk.Label(ventana, text="Seleccione un cliente/proveedor registrado por la recepcionista:", font=("Arial", 12)).pack(pady=10)
    combo_seleccion = ttk.Combobox(ventana, values=opciones, state="readonly")
    combo_seleccion.set("Seleccione un cliente/proveedor")
    combo_seleccion.pack(pady=10)
    
    tk.Button(ventana, text="Crear Cliente/Proveedor", command=crear_cliente_proveedor).pack(pady=10)

def abrir_formulario_empacador(root):
    ventana = tk.Toplevel(root)
    ventana.title("Formulario Empacador")
    centrar_ventana(ventana, 800, 400)  

    def generar_etiqueta():
        idx = combo_seleccion.current()
        if idx != -1:
            cliente_proveedor = registros[idx]
            etiqueta_ventana = tk.Toplevel(ventana)
            etiqueta_ventana.title("Etiqueta")
            centrar_ventana(etiqueta_ventana, 800, 400) 
            tk.Label(etiqueta_ventana, text="Etiqueta para el Cliente/Proveedor", font=("Arial", 12, "bold")).pack(pady=10)
            detalles = {
                "Nombre": cliente_proveedor[1],
                "Apellido": cliente_proveedor[2],
                "Documento de identidad": cliente_proveedor[3],
                "Número telefónico": cliente_proveedor[4],
                "Dirección": cliente_proveedor[5],
                "Correo electrónico": cliente_proveedor[6],
            }
            for key, value in detalles.items():
                tk.Label(etiqueta_ventana, text=f"{key}: {value}").pack(anchor="w", padx=10, pady=2)
    
    registros = obtener_clientes_proveedores()
    opciones = [f"{i + 1}. {reg[1]} {reg[2]}" for i, reg in enumerate(registros)]
    
    tk.Label(ventana, text="Seleccione un cliente/proveedor:", font=("Arial", 12)).pack(pady=10)
    combo_seleccion = ttk.Combobox(ventana, values=opciones, state="readonly")
    combo_seleccion.set("Seleccione un cliente/proveedor")
    combo_seleccion.pack(pady=10)
    
    tk.Button(ventana, text="Generar Etiqueta", command=generar_etiqueta).pack(pady=10)

def abrir_formulario_transportador(root):
    ventana = tk.Toplevel(root)
    ventana.title("Formulario Transportador")
    centrar_ventana(ventana, 800, 400)  

    def consultar_envio():
        idx = combo_seleccion.current()
        if idx != -1:
            cliente_proveedor = registros[idx]
            estados = ["En bodega", "Enviado", "En tránsito", "Cerca a tu dirección"]
            estado_actual = random.choice(estados)
            envio_ventana = tk.Toplevel(ventana)
            envio_ventana.title("Estado del Envío")
            centrar_ventana(envio_ventana, 800, 400)  
            detalles = {
                "Nombre": cliente_proveedor[1],
                "Apellido": cliente_proveedor[2],
                "Documento de identidad": cliente_proveedor[3],
                "Número telefónico": cliente_proveedor[4],
                "Dirección": cliente_proveedor[5],
                "Correo electrónico": cliente_proveedor[6],
            }
            tk.Label(envio_ventana, text="Información del Cliente/Proveedor:", font=("Arial", 12)).pack(pady=10)
            for key, value in detalles.items():
                tk.Label(envio_ventana, text=f"{key}: {value}").pack(anchor="w", padx=10, pady=2)
            tk.Label(envio_ventana, text=f"\nEstado del envío: {estado_actual}", font=("Arial", 12, "bold")).pack(pady=10)
    
    registros = obtener_clientes_proveedores()
    opciones = [f"{i + 1}. {reg[1]} {reg[2]}" for i, reg in enumerate(registros)]
    
    tk.Label(ventana, text="Seleccione un cliente/proveedor:", font=("Arial", 12)).pack(pady=10)
    combo_seleccion = ttk.Combobox(ventana, values=opciones, state="readonly")
    combo_seleccion.set("Seleccione un cliente/proveedor")
    combo_seleccion.pack(pady=10)
    
    tk.Button(ventana, text="Consultar Envío", command=consultar_envio).pack(pady=10)

def abrir_formulario_recepcionista(root):
    ventana = tk.Toplevel(root)
    ventana.title("Formulario Recepcionista")
    centrar_ventana(ventana, 800, 400) 
    crear_formulario(ventana, "Cliente/Distribuidor")

def crear_formulario(ventana, tipo):
    tk.Label(ventana, text=f"Formulario para {tipo}", font=("Arial", 12)).pack(pady=10)
    
    labels = ["Nombre", "Apellido", "Documento de identidad o NIT", "Número telefónico", "Dirección", "Correo electrónico"]
    entries = {}
    
    for label in labels:
        tk.Label(ventana, text=label).pack(anchor="w", padx=10)
        entry = tk.Entry(ventana, width=40)
        entry.pack(padx=10, pady=5)
        entries[label] = entry

    tk.Button(ventana, text="Guardar", command=lambda: guardar_informacion_recepcionista(entries)).pack(pady=10)

def guardar_informacion_recepcionista(entries):
    nombre = entries["Nombre"].get()
    apellido = entries["Apellido"].get()
    documento_identidad = entries["Documento de identidad o NIT"].get()
    numero_telefonico = entries["Número telefónico"].get()
    direccion = entries["Dirección"].get()
    correo_electronico = entries["Correo electrónico"].get()

    # Validar que ningún campo esté vacío
    if not nombre or not apellido or not documento_identidad or not numero_telefonico or not direccion or not correo_electronico:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    insertar_cliente_proveedor(nombre, apellido, documento_identidad, numero_telefonico, direccion, correo_electronico)

    messagebox.showinfo("Confirmación", f"Información guardada correctamente.")

    print(f"Información de Recepcionista guardada")
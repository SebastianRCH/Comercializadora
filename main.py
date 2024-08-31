import tkinter as tk
from tkinter import ttk
from auth import autenticar_usuario
from forms import (
    abrir_formulario_gerente,
    abrir_formulario_administrador,
    abrir_formulario_empacador,
    abrir_formulario_transportador,
    abrir_formulario_recepcionista
)
from db import inicializar_db

def centrar_ventana(ventana, ancho, alto):

    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    

    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def iniciar_sesion(root):
    ventana_login = tk.Toplevel(root)
    ventana_login.title("Inicio de Sesión")
    centrar_ventana(ventana_login, 800, 400) 
    
    tk.Label(ventana_login, text="Nombre de usuario").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack(pady=5)
    
    tk.Label(ventana_login, text="Contraseña").pack(pady=5)
    entry_password = tk.Entry(ventana_login, show="*")
    entry_password.pack(pady=5)
    
    def verificar_credenciales():
        username = entry_usuario.get()
        password = entry_password.get()
        if autenticar_usuario(username, password):
            tk.Label(ventana_login, text="Acceso concedido", fg="green").pack(pady=5)
            ventana_login.destroy()
            mostrar_menu_principal(root)
        else:
            tk.Label(ventana_login, text="Acceso denegado", fg="red").pack(pady=5)
    
    tk.Button(ventana_login, text="Iniciar Sesión", command=verificar_credenciales).pack(pady=10)

def mostrar_menu_principal(root):
    root.withdraw() 
    
    ventana_menu = tk.Toplevel(root)
    ventana_menu.title("Menú Principal")
    centrar_ventana(ventana_menu, 800, 400)
    ventana_menu.protocol("WM_DELETE_WINDOW", lambda: (ventana_menu.destroy(), root.deiconify())) 

    roles = ["Gerente", "Administrador", "Empacador", "Transportador", "Recepcionista"]
    combo = ttk.Combobox(ventana_menu, values=roles, state="readonly")
    combo.set("Selecciona un rol")
    combo.pack(pady=10)

    def abrir_formulario():
        rol = combo.get()
        if rol == "Recepcionista":
            abrir_formulario_recepcionista(root)
        elif rol == "Administrador":
            abrir_formulario_administrador(root)
        elif rol == "Empacador":
            abrir_formulario_empacador(root)
        elif rol == "Transportador":
            abrir_formulario_transportador(root)
        elif rol == "Gerente":
            abrir_formulario_gerente(root)

    mostrar_button = tk.Button(ventana_menu, text="Abrir Formulario", command=abrir_formulario)
    mostrar_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Formularios por Rol")
    
    inicializar_db()
    iniciar_sesion(root)

    root.mainloop()
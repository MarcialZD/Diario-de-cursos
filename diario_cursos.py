import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from datetime import datetime
import os

# Obtener el directorio del archivo Python actual
current_directory = os.path.dirname(__file__)
diarios_directory = os.path.join(current_directory, "diarios")

# Crear la carpeta de diarios si no existe
if not os.path.exists(diarios_directory):
    os.makedirs(diarios_directory)

# Función para guardar la entrada en el archivo de texto del curso seleccionado
def guardar_entrada():
    entrada = text_area.get("1.0", tk.END).strip()
    if entrada and current_course.get():
        course_file = os.path.join(diarios_directory, f"{current_course.get()}.txt")
        with open(course_file, "a") as file:
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"\n[{fecha_hora}] {entrada}\n")
        text_area.delete("1.0", tk.END)
        messagebox.showinfo("Éxito", "Registro guardado exitosamente")  # Mensaje en ventana emergente

# Función para añadir un nuevo curso
def añadir_curso():
    nuevo_curso = simpledialog.askstring("Añadir curso", "Nombre del nuevo curso:")
    if nuevo_curso:
        nuevo_curso = nuevo_curso.strip()
        if nuevo_curso:
            course_listbox.insert(tk.END, nuevo_curso)
            messagebox.showinfo("Éxito", "Curso añadido exitosamente")  # Mensaje en ventana emergente

# Función para seleccionar un curso
def seleccionar_curso(event):
    seleccion = course_listbox.curselection()
    if seleccion:
        curso_seleccionado = course_listbox.get(seleccion[0])
        current_course.set(curso_seleccionado)

# Función para ver los registros del curso seleccionado
def ver_registros():
    if current_course.get():
        course_file = os.path.join(diarios_directory, f"{current_course.get()}.txt")
        if os.path.exists(course_file):
            with open(course_file, "r") as file:
                registros = file.read()
            registros_window = tk.Toplevel(root)
            registros_window.title(f"Registros de {current_course.get()}")
            registros_text = scrolledtext.ScrolledText(registros_window, wrap=tk.WORD, width=50, height=20)
            registros_text.pack(padx=10, pady=10)
            registros_text.insert(tk.END, registros)
            registros_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Información", "No hay registros para este curso.") 
             # Mensaje en ventana emergente
    else:
        messagebox.showwarning("Advertencia", "Seleccione un curso primero.") 
         # Mensaje en ventana emergente

# Función para eliminar el curso seleccionado
def eliminar_curso():
    seleccion = course_listbox.curselection()
    if seleccion:
        curso_seleccionado = course_listbox.get(seleccion[0])
        confirmar = messagebox.askyesno("Eliminar curso", f"¿Está seguro de que desea eliminar el curso '{curso_seleccionado}'?")
        if confirmar:
            course_file = os.path.join(diarios_directory, f"{curso_seleccionado}.txt")
            if os.path.exists(course_file):
                os.remove(course_file)
            course_listbox.delete(seleccion[0])
            current_course.set("")
            messagebox.showinfo("Éxito", f"Curso '{curso_seleccionado}' eliminado exitosamente.")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un curso primero.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Diario de Cursos")

# Variable para el curso actual
current_course = tk.StringVar()

# Frame para los cursos
course_frame = tk.Frame(root)
course_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Listbox para mostrar los cursos disponibles
course_listbox = tk.Listbox(course_frame, height=10, width=50)
course_listbox.pack(padx=10, pady=10)
course_listbox.bind("<<ListboxSelect>>", seleccionar_curso)

# Cargar los cursos existentes en la lista
for archivo in os.listdir(diarios_directory):
    if archivo.endswith(".txt"):
        course_listbox.insert(tk.END, archivo.replace(".txt", ""))

# Botones para añadir y eliminar cursos
course_buttons_frame = tk.Frame(course_frame)
course_buttons_frame.pack(pady=5)

añadir_curso_btn = tk.Button(course_buttons_frame, text="Añadir Curso", command=añadir_curso)
añadir_curso_btn.pack(side=tk.LEFT, padx=5)

eliminar_curso_btn = tk.Button(course_buttons_frame, text="Eliminar Curso", command=eliminar_curso)
eliminar_curso_btn.pack(side=tk.LEFT, padx=5)

# Frame para el área de texto y botones
entry_frame = tk.Frame(root)
entry_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Área de texto
text_area = scrolledtext.ScrolledText(entry_frame, wrap=tk.WORD, width=50, height=20)
text_area.pack(padx=10, pady=10)

# Botones para guardar y ver registros
entry_buttons_frame = tk.Frame(entry_frame)
entry_buttons_frame.pack(pady=5)

guardar_btn = tk.Button(entry_buttons_frame, text="Guardar", command=guardar_entrada)
guardar_btn.pack(side=tk.LEFT, padx=5)

ver_registros_btn = tk.Button(entry_buttons_frame, text="Ver Registros", command=ver_registros)
ver_registros_btn.pack(side=tk.LEFT, padx=5)

# Ejecutar la interfaz
root.mainloop()

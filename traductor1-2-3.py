import json
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

def cargar_datos(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'ESPAÑOL': {}, 'INGLES': {}, 'ERRORES': {}}

def guardar_datos(datos, archivo):
    with open(archivo, 'w', encoding='utf-8') as file:
        json.dump(datos, file, indent=4, ensure_ascii=False, sort_keys=True)

def distancia_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def obtener_sugerencias(datos, palabra, idioma):
    errores = datos['ERRORES']
    diccionario = datos[idioma]
    todas_las_palabras = list(diccionario.keys())
    correcciones_previas = [err for err, corrs in errores.items() if palabra in corrs]
    sugerencias_previas = correcciones_previas + todas_las_palabras
    sugerencias_por_distancia = sorted(
        set(sugerencias_previas),
        key=lambda p: (p not in correcciones_previas, distancia_levenshtein(p, palabra))
    )
    return sugerencias_por_distancia[:3]

class TraductorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Traductor")
        
        self.datos = cargar_datos("Traducciones.json")
        
        tk.Label(master, text="Seleccione el idioma a traducir:").grid(row=0, column=0)
        self.idioma_var = tk.StringVar(master)
        self.idioma_var.set("ESPAÑOL")
        tk.OptionMenu(master, self.idioma_var, "ESPAÑOL", "INGLES").grid(row=0, column=1)
        
        tk.Label(master, text="Introduce una palabra para traducir:").grid(row=1, column=0)
        self.palabra_entry = tk.Entry(master)
        self.palabra_entry.grid(row=1, column=1)
        
        self.translate_button = tk.Button(master, text="Traducir", command=self.traducir)
        self.translate_button.grid(row=2, columnspan=2)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=3, columnspan=2)

        self.sugerencias_listbox = tk.Listbox(master)
        self.sugerencias_listbox.grid(row=4, columnspan=2)
        self.sugerencias_listbox.bind('<<ListboxSelect>>', self.on_sugerencia_seleccionada)

    def traducir(self):
        idioma = self.idioma_var.get()
        palabra_usuario = self.palabra_entry.get().upper()

        idioma_destino = 'INGLES' if idioma == 'ESPAÑOL' else 'ESPAÑOL'
        diccionario = self.datos[idioma_destino]
        if palabra_usuario in diccionario:
            traduccion = diccionario[palabra_usuario]
            self.result_label.config(text=f"La palabra '{palabra_usuario}' se traduce como '{traduccion}'")
            self.sugerencias_listbox.delete(0, tk.END)
        else:
            if palabra_usuario in self.datos['ERRORES']:
                sugerencias = obtener_sugerencias(self.datos, palabra_usuario, idioma_destino)
                if not sugerencias:
                    self.result_label.config(text=f"No se encontró la palabra '{palabra_usuario}'.")
                else:
                    self.mostrar_sugerencias(sugerencias)
            else:
                self.agregar_nueva_palabra(palabra_usuario, idioma_destino)

    def mostrar_sugerencias(self, sugerencias):
        self.sugerencias_listbox.delete(0, tk.END)
        for sug in sugerencias:
            self.sugerencias_listbox.insert(tk.END, sug)
        self.result_label.config(text="Selecciona una sugerencia dado que se trata de un error:")

    def agregar_nueva_palabra(self, palabra, idioma_destino):
        traduccion = simpledialog.askstring("Nueva Traducción", f"Introduce la traducción para '{palabra}':")
        if traduccion:
            self.datos[idioma_destino][palabra] = traduccion.upper()
            self.result_label.config(text=f"Traducción añadida: {palabra} -> {traduccion}")
            guardar_datos(self.datos, "Traducciones.json")
        else:
            self.result_label.config(text="No se proporcionó traducción.")


    def on_sugerencia_seleccionada(self, event):
        try:
            index = self.sugerencias_listbox.curselection()[0]
            sugerencia = self.sugerencias_listbox.get(index)
            self.palabra_entry.delete(0, tk.END)  # Opcional: limpiar la entrada
            self.palabra_entry.insert(0, sugerencia)  # Opcional: insertar la sugerencia en el campo de entrada

            idioma = self.idioma_var.get()
            idioma_destino = 'INGLES' if idioma == 'ESPAÑOL' else 'ESPAÑOL'
            diccionario = self.datos[idioma_destino]

            if sugerencia in diccionario:
                traduccion = diccionario[sugerencia]
                self.result_label.config(text=f"La palabra '{sugerencia}' se traduce como '{traduccion}'.")
            else:
                traduccion = simpledialog.askstring("Traducción", f"No se conoce la traducción para '{sugerencia}'. Introduce su traducción:")
                if traduccion:
                    diccionario[sugerencia] = traduccion.upper()
                    self.result_label.config(text=f"Traducción añadida: {sugerencia} -> {traduccion}")
                    self.datos[idioma_destino] = diccionario  # Asegurarse de que el diccionario actualizado se guarda
                    guardar_datos(self.datos, "Traducciones.json")
                else:
                    self.result_label.config(text="No se proporcionó traducción.")

            # Recordar la corrección para futuras referencias
            palabra_usuario = self.palabra_entry.get().upper()
            self.datos['ERRORES'].setdefault(palabra_usuario, []).append(sugerencia)
            guardar_datos(self.datos, "Traducciones.json")

        except IndexError:
            self.result_label.config(text="No se seleccionó ninguna sugerencia.")


root = tk.Tk()
app = TraductorApp(root)
root.mainloop()

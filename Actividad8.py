import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt



MainWindow = tk.Tk()
MainWindow.title("Votaciones")
MainWindow.geometry("800x600")

votantes = []
juradospormesa = []
cedulasjurados = set()
cedulasvotantes = set()
resultadosvotacion = []
asistencias = []



def guardadatosvotaciones():
    archivo = open("DatosVotaciones.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(archivo)

    writer.writerow(["------------Centro de Votación-----------\n"])
    writer.writerow(["Cantidad de Salones", entry_salon.get()])
    writer.writerow(["Cantidad de Mesas por Salón", entry_mesas.get()])
    writer.writerow(["Cantidad de Jurados por Mesa", entry_jurados.get()])
    writer.writerow([])

    writer.writerow(["---------Jurados por Mesa--------\n"])
    for i, jurados in enumerate(juradospormesa):
        for jurado in jurados:
            writer.writerow([f"Mesa {i+1}", jurado[0], jurado[1], jurado[2], jurado[3]])
    writer.writerow([])

    writer.writerow(["-----------Votantes---------\n"])
    for v in votantes:
        writer.writerow([v["nombre"], v["cedula"], v["salon"], v["mesa"]])

    archivo.close()
    messagebox.showinfo("Los datos fueron guardados exitosamente en 'DatosVotaciones.csv'")

def cargarvotantes():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de votantes", filetypes=[("CSV files", "*.csv")])
    if archivo != "":
        with open(archivo, newline='', encoding='utf-8') as f:
            lector = csv.reader(f)
            next(lector, None)
            votantes.clear()
            cedulasvotantes.clear()
            for fila in lector:
                if len(fila) >= 4:
                    cedula = fila[1].strip()
                    if cedula in cedulasvotantes:
                        messagebox.showerror("Error", f"Cédula duplicada detectada: {cedula}")
                        return
                    votantes.append({
                        "nombre": fila[0].strip(),
                        "cedula": cedula,
                        "salon": fila[2].strip().lower(),
                        "mesa": fila[3].strip().lower()
                    })
                    cedulasvotantes.add(cedula)
        messagebox.showinfo("Carga exitosa", "Votantes cargados correctamente.")
    else:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")

def buscarvotante():
    cedula = EntryBuscarVotante.get()
    if cedula == "":
        messagebox.showerror("Error", "Por favor, ingrese una cédula.")
        return
    for v in votantes:
        if v["cedula"] == cedula:
            messagebox.showinfo("Votante encontrado", f"Nombre: {v['nombre']}\nCédula: {v['cedula']}\nSalon: {v['salon']}\nMesa: {v['mesa']}")
            return
    messagebox.showerror("Error", "No se encontró el votante.")

def mostrardatosjurados(indicemesa):
    jurados = juradospormesa[indicemesa]
    if jurados == []:
        messagebox.showerror("Error", "No hay jurados registrados para esta mesa.")
        return

    totalmesas = int(entry_mesas.get())
    salonnum = (indicemesa // totalmesas) + 1
    mesanum = (indicemesa % totalmesas) + 1

    salida = ""
    for i, jurado in enumerate(jurados):
        salida += f"Jurado #{i+1}:\nNombre: {jurado[0]}\nCédula: {jurado[1]}\nTeléfono: {jurado[2]}\nDirección: {jurado[3]}\n\n"

    nombremesa = f"mesa {mesanum}".lower()
    nombresalon = f"salón {salonnum}".lower()

    votantesenmesa = [v for v in votantes if v["mesa"] == nombremesa and v["salon"] == nombresalon]

    if votantesenmesa == []:
        salida += " No hay votantes asignados a esta mesa"
    else:
        salida += " Votantes \n"
        for v in votantesenmesa:
            salida += f"Nombre: {v['nombre']}\nCédula: {v['cedula']}\n\n"

    messagebox.showinfo(f"Datos del Salón {salonnum} - Mesa {mesanum}", salida)

def guardardatos(entradas, FrameFormulario, indicemesa):
    DatosGuardados = []

    for entry in entradas:
        if entry.get() == "":
            messagebox.showerror("Error, Por favor, complete todos los campos.")
            return

    cedula = entradas[1].get().strip()
    if cedula in cedulasjurados:
        messagebox.showerror("Error, La cédula del jurado ya ha sido registrada.")
        return

    for entry in entradas:
        DatosGuardados.append(entry.get())

    juradospormesa[indicemesa].append(DatosGuardados)
    cedulasjurados.add(cedula)

    label = tk.Label(FrameFormulario, text="Los datos han sido guardados correctamente")
    label.pack()

def formulariojurado(indicemesa):
    FrameFormulario = tk.Toplevel(MainWindow)
    FrameFormulario.title(f"Formulario Jurado - Mesa {indicemesa + 1}")
    FrameFormulario.geometry("300x400")

    campos = ["Nombre", "Cédula", "Teléfono", "Dirección"]
    entradas = []

    for campo in campos:
        label = tk.Label(FrameFormulario, text=f"{campo}:")
        label.pack()
        entryF = tk.Entry(FrameFormulario)
        entryF.pack()
        entradas.append(entryF)

    botonguardar = tk.Button(FrameFormulario, text="Guardar", command=lambda: guardardatos(entradas, FrameFormulario, indicemesa))
    botonguardar.pack()

def generarvotacion():
    for Eliminar in ContenedorSalon.winfo_children():
        Eliminar.destroy()

    try:
        totalsalones = int(entry_salon.get())
        totalmesas = int(entry_mesas.get())
        total_jurados = int(entry_jurados.get())
        if totalsalones <= 0 or totalmesas <= 0 or total_jurados <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingrese números enteros positivos para salones, mesas y jurados.")
        return

    juradospormesa.clear()
    totalmesastotal = totalsalones * totalmesas

    for _ in range(totalmesastotal):
        juradospormesa.append([])

    indicemesa_global = 0

    for i in range(totalsalones):
        frame_salon = tk.LabelFrame(ContenedorSalon, text=f"Salón {i+1}")
        frame_salon.grid(row=i, column=2)

        for m in range(totalmesas):
            framemesa = tk.Frame(frame_salon)
            framemesa.pack()

            btnmesa = tk.Button(framemesa, text=f"Mesa {m+1}", width=10,
                                 command=lambda index=indicemesa_global: mostrardatosjurados(index))
            btnmesa.pack(side="left")

            for j in range(total_jurados):
                btn_jurado = tk.Button(framemesa, text=f"Jurado {j+1}", width=10,
                                       command=lambda index=indicemesa_global: formulariojurado(index))
                btn_jurado.pack(side="left")

            indicemesa_global += 1

def registrar_asistencia():
    ventana = tk.Toplevel(MainWindow)
    ventana.title("Registrar Asistencia")
    ventana.geometry("300x300")

    tk.Label(ventana, text="Cédula:").pack()
    entry_cedula = tk.Entry(ventana)
    entry_cedula.pack()

    tk.Label(ventana, text="Salón:").pack()
    entry_salon_as = tk.Entry(ventana)
    entry_salon_as.pack()

    tk.Label(ventana, text="Mesa:").pack()
    entry_mesa_as = tk.Entry(ventana)
    entry_mesa_as.pack()

    tk.Label(ventana, text="Hora (HH:MM):").pack()
    entry_hora = tk.Entry(ventana)
    entry_hora.pack()

    def guardar_asistencia():
        cedula = entry_cedula.get().strip()
        salon = entry_salon_as.get().strip().lower()
        mesa = entry_mesa_as.get().strip().lower()
        hora = entry_hora.get().strip()

        if not cedula or not salon or not mesa or not hora:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            horas, minutos = map(int, hora.split(":"))
            if horas > 16 or (horas == 16 and minutos > 0):
                raise ValueError
        except:
            messagebox.showerror("Error", "Hora inválida o mayor a las 4:00 PM.")
            return

        if cedula not in cedulasvotantes:
            messagebox.showerror("Error", "La cédula no corresponde a ningún votante.")
            return

        asistencias.append({
            "cedula": cedula,
            "salon": salon,
            "mesa": mesa,
            "hora": hora
        })
        messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")
        ventana.destroy()

    tk.Button(ventana, text="Registrar", command=guardar_asistencia).pack()


def cargar_resultados():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de resultados", filetypes=[("Archivos", "*.csv *.json")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return

    resultadosvotacion.clear()
    try:
        if archivo.endswith(".csv"):
            with open(archivo, newline='', encoding='utf-8') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    resultadosvotacion.append(fila)
        elif archivo.endswith(".json"):
            with open(archivo, 'r', encoding='utf-8') as f:
                resultadosvotacion.extend(json.load(f))
        else:
            raise ValueError("Formato no soportado")
        messagebox.showinfo("Éxito", "Resultados cargados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los resultados:\n{e}")

def buscarjurado():
    cedula = EntryBuscarJurado.get()
    if cedula == "":
        messagebox.showerror("Error, Por favor, ingrese una cédula.")
        return
    for i, jurados in enumerate(juradospormesa):
        for jurado in jurados:
            if jurado[1] == cedula:
                salonnum = (i // int(entry_mesas.get())) + 1
                mesanum = (i % int(entry_mesas.get())) + 1
                messagebox.showinfo("Jurado encontrado",
                                    f"Nombre: {jurado[0]}\nCédula: {jurado[1]}\nTeléfono: {jurado[2]}\nDirección: {jurado[3]}\nAsignado a Salón {salonnum}, Mesa {mesanum}")
                return
    messagebox.showerror("Error, No se encontró el jurado.")

def generarestadisticas():
    if not resultadosvotacion:
        messagebox.showerror("Error, No hay resultados de votación cargados.")
        return

    try:
        rv = pd.DataFrame(resultadosvotacion)

        preguntas = [col for col in rv.columns if col.startswith('p')]
        resumen = ""

        for pregunta in preguntas:
            conteo = rv[pregunta].value_counts()
            resumen += f"{pregunta.upper()}:\n"
            resumen += f"  Sí: {conteo.get('Sí', 0)}\n"
            resumen += f"  No: {conteo.get('No', 0)}\n\n"

        conteomesas = rv.groupby(['salon', 'mesa']).size()
        resumen += "--- Total de votos por mesa ---\n"
        for (salon, mesa), total in conteomesas.items():
            resumen += f"Salón {salon}, Mesa {mesa}: {total} votos\n"

        messagebox.showinfo("Resumen Estadístico", resumen)

    except Exception as e:
        messagebox.showerror(f"Error No se pudo generar el resumen:\n{e}")

def guardarresumencsv():
    if not resultadosvotacion:
        messagebox.showerror("Error, No hay resultados para guardar.")
        return

    try:
        rv = pd.DataFrame(resultadosvotacion)
        nombrearchivo = filedialog.asksaveasfilename(defaultextension=".csv", title="Guardar resumen", filetypes=[("CSV files", "*.csv")])
        if nombrearchivo:
            rv.to_csv(nombrearchivo, index=False)
            messagebox.showinfo("Éxito", f"Resumen guardado en {nombrearchivo}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

def graficarresultados():
    if not resultadosvotacion:
        messagebox.showerror("Error", "No hay resultados cargados.")
        return

    try:
        rv = pd.DataFrame(resultadosvotacion)
        preguntas = [col for col in rv.columns if col.startswith('p')]

        si = []
        no = []
        for p in preguntas:
            si.append(rv[p].value_counts().get("Sí", 0))
            no.append(rv[p].value_counts().get("No", 0))

        x = range(len(preguntas))
        plt.bar(x, si, width=0.4, label='Sí', align='center', color='green')
        plt.bar([i + 0.4 for i in x], no, width=0.4, label='No', align='center', color='red')
        plt.xticks([i + 0.2 for i in x], preguntas)
        plt.ylabel("Cantidad de votos")
        plt.title("Resultados por pregunta")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo graficar:\n{e}")


tk.Button(MainWindow, text="Resumen Estadístico", command=generarestadisticas).grid(row=11, column=0)
tk.Button(MainWindow, text="Guardar Resumen CSV", command=guardarresumencsv).grid(row=11, column=1)
tk.Button(MainWindow, text="Visualizar Resultados", command=graficarresultados).grid(row=11, column=2)


tk.Button(MainWindow, text="Registrar Asistencia", command=registrar_asistencia).grid(row=8, column=0)
tk.Button(MainWindow, text="Cargar Resultados", command=cargar_resultados).grid(row=9, column=0)

tk.Label(MainWindow, text="Buscar Jurado por Cédula:").grid(row=10, column=0)
EntryBuscarJurado = tk.Entry(MainWindow)
EntryBuscarJurado.grid(row=10, column=1)
tk.Button(MainWindow, text="Buscar", command=buscarjurado).grid(row=10, column=2)


titulo = tk.Label(MainWindow, text="VOTACIONES", font=("Arial", 18, "bold"))
titulo.grid(row=0, column=0)

tk.Label(MainWindow, text="Numero de salones:").grid(row=1, column=0)
entry_salon = tk.Entry(MainWindow)
entry_salon.grid(row=1, column=1)

tk.Label(MainWindow, text="Numero de Mesas por Salón:").grid(row=2, column=0)
entry_mesas = tk.Entry(MainWindow)
entry_mesas.grid(row=2, column=1)

tk.Label(MainWindow, text="Numero de Jurados por Mesa:").grid(row=3, column=0)
entry_jurados = tk.Entry(MainWindow)
entry_jurados.grid(row=3, column=1)

tk.Button(MainWindow, text="Generar Centro de Votación", command=generarvotacion).grid(row=4, column=0)
tk.Button(MainWindow, text="Guardar centro de votacion", command=guardadatosvotaciones).grid(row=5, column=0)
tk.Button(MainWindow, text="Cargar Centro de votacion").grid(row=6, column=0)
tk.Button(MainWindow, text="Cargar Datos votantes", command=cargarvotantes).grid(row=7, column=0)

tk.Label(MainWindow, text="Buscar Votante por Cédula:").grid(row=8, column=0)
EntryBuscarVotante = tk.Entry(MainWindow)
EntryBuscarVotante.grid(row=8, column=1)
tk.Button(MainWindow, text="Buscar", command=buscarvotante).grid(row=8, column=2)

ContenedorSalon = tk.Frame(MainWindow)
ContenedorSalon.grid(row=9, column=0)

MainWindow.mainloop()

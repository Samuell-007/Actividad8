# Sistema de Votación con Interfaz Gráfica

Este es un sistema de gestión de votaciones desarrollado en Python con Tkinter. Permite organizar salones, mesas, jurados y votantes en un centro de votación. También incluye funciones para cargar resultados, registrar asistencia y generar estadísticas con visualización.

# Funcionalidades

Registro de jurados por mesa  
Asignación de salones, mesas y jurados dinámicamente  
Carga de votantes desde archivo CSV  
Búsqueda de votantes y jurados por cédula  
Registro de asistencia (con validación de hora ≤ 4:00 PM)  
Carga de resultados desde archivo .csv o .json  
Resumen estadístico con pandas  
Visualización gráfica con matplotlib  
Exportación de resultados a archivo CSV

# Requisitos

- Visual Studio Code con phyton, pandas, CSV
- Librerías necesarias:

 tkinter:
-  messagebox
-  filedialog
csv
json
pandas
matplotlib.pyplot

# Antes de ejecutar el codigo debes

instalar las bibliotecas necesarias con pip directamente en la terminal:

pip install pandas 
pip install matplotlib

# Pasos

Ejecuta el archivo principal:

- Ingresa el número de salones (ej. 2)
- Ingresa el número de mesas por salón (ej. 3)
- Ingresa el número de jurados por mesa (ej. 2)
- Haz clic en: "Generar Centro de Votación"
- 

Haz clic en un botón "Jurado 1", "Jurado 2", etc.
Llena el formulario:
- Nombre
- Cédula
- Teléfono
- Dirección
Haz clic en "Guardar"
# Las cédulas duplicadas serán rechazadas.


Haz clic en "Cargar Datos Votantes"
Selecciona un archivo CSV con columnas:
    nombre, cedula, salon, mesa
Ejemplo de nombres válidos:
    salón 1, mesa 2

- Escribe una cédula en el campo correspondiente
- Haz clic en "Buscar"
- Se mostrará el nombre, salón y mesa si está registrado



Haz clic en "Registrar Asistencia"
Completa el formulario:
    - Cédula
    - Salón
    - Mesa
    - Hora 
  Hora máxima permitida: 16:00pm o 04:00pm


Escribe la cédula del jurado en el campo correspondiente
Haz clic en "Buscar"
Se mostrará su asignación


Haz clic en el botón "Mesa 1"
Se mostrará:
    - Jurados registrados
    - Votantes asignados


Haz clic en "Cargar Resultados"
Selecciona archivo CSV o JSON con votos (p1 a p9)



"Resumen Estadístico": muestra conteos por pregunta
"Guardar Resumen CSV": exporta resultados
"Visualizar Resultados": muestra gráfico de barras


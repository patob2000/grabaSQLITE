#Quiero que me crees python que lee un XLSX  y graba registros en un base sqlite3 en memoria.

#Salta la primera fila del encabezado del archivo XLSX
#El archivo XLSX se llama "respuestas.xlsx"
#Borra el contenido de la tabla si ya existe.
#El commit y el close hazlo al final para acelerar el proceso.

#Crear una tabla :  "respuestas" 
# "nombre" string = columna NOMBRES + APELLIDOS
# "pregunta" string = columna DESC_PREGUNTA
# "respuesta" string = columna DESC_RESPUESTA si es el valor es diferente de NULL o RESPUESTA_ABIERTA si el valor es diferente de NULL

#Ejemplo del archivo XLSX :

#PERIODO;PIDM;RUT_DOCENTE;NOMBRES;APELLIDOS;NRC;ENCUESTA;COD_PREGUNTA;DESC_PREGUNTA;DESC_RESPUESTA;RESPUESTA_ABIERTA
#202332;59.618.912;136344773;ANGELICA MARIA;BARRIA/DIAZ;10985;EDTECHT2;EVD25;¿Cómo calificas el Desempeño global del docente en la asignatura? (escribe: Destacado, Competente, Básico o Insatisfactorio);NULL;compente
#202332;59.618.912;136344773;ANGELICA MARIA;BARRIA/DIAZ;10985;EDTECHT2;EVD25;¿Cómo calificas el Desempeño global del docente en la asignatura? (escribe: Destacado, Competente, Básico o Insatisfactorio);NULL;basico
#202332;59.618.912;136344773;ANGELICA MARIA;BARRIA/DIAZ;10985;EDTECHT2;EVD25;¿Cómo calificas el Desempeño global del docente en la asignatura? (escribe: Destacado, Competente, Básico o Insatisfactorio);NULL;Destacado


import csv
import sqlite3

# Conexión a la base de datos en memoria
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Borrar tabla si ya existe
cursor.execute("DROP TABLE IF EXISTS respuestas")

# Crear la tabla respuestas
cursor.execute('''
CREATE TABLE respuestas (
    nombre TEXT,
    pregunta TEXT,
    respuesta TEXT
)
''')

# Leer el archivo CSV
with open('respuestas.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    
    # Saltar el encabezado
    next(reader)
    
    for row in reader:
        nombres = row[3]
        apellidos = row[4]
        desc_pregunta = row[8]
        desc_respuesta = row[9]
        respuesta_abierta = row[10]

        # Construir el valor para la columna "nombre"
        nombre_completo = f"{nombres} {apellidos}"

        # Decidir qué valor usar para la columna "respuesta"
        if desc_respuesta != 'NULL':
            respuesta = desc_respuesta
        else:
            respuesta = respuesta_abierta

        # Insertar en la base de datos
        cursor.execute('''
            INSERT INTO respuestas (nombre, pregunta, respuesta)
            VALUES (?, ?, ?)
        ''', (nombre_completo, desc_pregunta, respuesta))

# Realizar la consulta que me diste
cursor.execute('''
SELECT nombre, pregunta, respuesta, COUNT(*) as contador
FROM respuestas
WHERE nombre like '%LUIS%' and respuesta in ('En total desacuerdo','De acuerdo','Medianamente de acuerdo','Totalmente de acuerdo','') 
GROUP BY pregunta
ORDER BY pregunta DESC;
''')

# Mostrar los resultados
resultados = cursor.fetchall()
for row in resultados:
    print(row)

# Realizar commit y cerrar la conexión
conn.commit()
conn.close()

print("\nConsulta realizada y resultados mostrados.")





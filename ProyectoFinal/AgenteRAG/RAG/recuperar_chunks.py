import pyodbc

def obtener_chunks_desde_sql(pregunta: str) -> str:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=RAG_Documentos;"
        "UID=rag_user;"
        "PWD=Rag1234!;"
    )
    cursor = conn.cursor()

    # Mapeo básico de preguntas a filtros SQL
    if "empresa" in pregunta or "perjuicio" in pregunta:
        cursor.execute("SELECT chunk FROM Chunks WHERE chunk LIKE '%Patito EC%' AND (chunk LIKE '%pérdida%' OR chunk LIKE '%impacto%' OR chunk LIKE '%afectación%');")
    elif "cronológico" in pregunta:
        cursor.execute("SELECT documento, fecha FROM Chunks ORDER BY fecha ASC;")
    elif "problema" in pregunta or "causa" in pregunta:
        cursor.execute("SELECT chunk FROM Chunks WHERE chunk LIKE '%problema%' OR chunk LIKE '%causa%' OR chunk LIKE '%incidente%';")
    elif "involucrado" in pregunta or "quién" in pregunta:
        cursor.execute("SELECT chunk FROM Chunks WHERE chunk LIKE '%Juanito Montero%' OR chunk LIKE '%Carlos Gómez%' OR chunk LIKE '%Sebastián Rivera%' OR chunk LIKE '%firma%';")
    elif "sanción" in pregunta or "sanciones" in pregunta:
        cursor.execute("SELECT chunk FROM Chunks WHERE chunk LIKE '%advertencia%' OR chunk LIKE '%sanción%' OR chunk LIKE '%suspendido%' OR chunk LIKE '%acción disciplinaria%';")
    else:
        cursor.execute("SELECT chunk FROM Chunks WHERE chunk LIKE ?", f"%{pregunta}%")

    resultados = cursor.fetchall()
    conn.close()

    contexto = "\n".join(row[0] for row in resultados[:5])  # limitar para no sobrecargar el prompt
    return contexto
# Prueba para obtener los chunks desde sql
#print(obtener_chunks_desde_sql("¿Qué tipo de problema fue, cuál fue la causa del incidente?"))

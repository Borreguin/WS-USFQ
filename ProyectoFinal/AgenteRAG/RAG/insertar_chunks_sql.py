import os
import pyodbc
from crear_chunks import procesar_directorio_pdf

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=RAG_Documentos;"
        "UID=rag_user;"
        "PWD=Rag1234!;"
    )
    cursor = conn.cursor()
    print("✅ Conexión exitosa a SQL Server")

    # Verificar que haya PDFs en el directorio
    archivos = os.listdir("../data")
    print("🗂️ Archivos encontrados en ../data:", archivos)

    # Procesar PDFs
    chunks = procesar_directorio_pdf("../data")
    print(f"📦 Total de chunks generados: {len(chunks)}")

    if len(chunks) == 0:
        print("⚠️ No se generaron chunks. Verifica que la carpeta ../RAG tenga archivos PDF.")

    # Imprimir ejemplo de chunks
    for ch in chunks[:2]:
        print("➡️ Chunk de ejemplo:", ch)

    # Insertar en la base de datos con manejo de errores
    errores = 0
    for i, ch in enumerate(chunks):
        try:
            cursor.execute(
                """
                INSERT INTO Chunks (documento, chunk, posicion, fecha)
                VALUES (?, ?, ?, ?)
                """,
                ch["documento"], ch["chunk"], ch["posicion"], ch["fecha"]
            )
        except Exception as ex:
            errores += 1
            print(f"❌ Error en chunk {i}: {ex}")
            print("📝 Datos del chunk con error:", ch)

    conn.commit()
    print(f"✅ Inserciones exitosas: {len(chunks) - errores}")
    print(f"❌ Errores totales: {errores}")

    # Verificar que se hayan insertado datos
    cursor.execute("SELECT TOP 3 * FROM Chunks ORDER BY id DESC")
    for row in cursor.fetchall():
        print("🔍 Registro insertado:", row)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Error de conexión o inserción:", e)


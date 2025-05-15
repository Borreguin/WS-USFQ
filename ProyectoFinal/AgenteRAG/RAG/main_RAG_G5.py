from ProyectoFinal.AgenteRAG.RAG.crear_chunks import procesar_directorio_pdf

ruta = "../data"
todos_los_chunks = procesar_directorio_pdf(ruta)

# Ejemplo: mostrar los primeros 2
for chunk in todos_los_chunks:
    print(chunk)

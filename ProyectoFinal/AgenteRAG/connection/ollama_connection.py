import asyncio
import json
import os
import httpx
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ReadPDF import contenido
from keyandcontext import KeyAndContext  # opcional si lo usas

# Configuración de Ollama
OLLAMA_URL = "http://localhost:11434/api/chat"
model_to_use = "llama3.2"  # Usa el modelo exacto que tengas en Ollama

# -----------------------------
# Función para llamar a Ollama
# -----------------------------
async def get_completion(prompt: str, model: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={"model": model, "messages": [{"role": "user", "content": prompt}]}
            )
            response.raise_for_status()
            full_content = ""
            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line)
                        message = json_data.get("message", {})
                        content = message.get("content", "")
                        full_content += content
                    except Exception as e:
                        print(f"Error processing chunk: {e}")
            return full_content.strip()
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error: no se pudo obtener respuesta del modelo."

# ----------------------------------
# Prompt universal para extracción
# ----------------------------------
def generar_prompt(texto_documento):
    return f"""
Extrae la siguiente información del siguiente texto, si está presente. Si no se encuentra, escribe "No encontrado" en el campo correspondiente. Devuelve la respuesta **exactamente en este formato**:

Empresa: ...
Perjuicio: ...
Tipo de problema: ...
Causa: ...
Involucrados: ...
Reporta: ...
Sanciones: ...

Texto:
{texto_documento}
"""

# ----------------------------------
# Procesar cada documento
# ----------------------------------
async def procesar_documentos(contenido_dict):
    resultados = []
    for nombre_archivo, paginas in contenido_dict.items():
        texto_completo = "\n".join(paginas.values())
        prompt = generar_prompt(texto_completo)
        print(f"📄 Procesando: {nombre_archivo}")
        respuesta = await get_completion(prompt, model_to_use)

        resultados.append({
            "archivo": nombre_archivo,
            "contenido": texto_completo[:500] + "...",  # opcional para referencia
            "extraccion": respuesta
        })

    return resultados

# ----------------------------------
# Guardar resultado como JSON
# ----------------------------------
def guardar_resultado_json(resultados, ruta="dataset_extraido.json"):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

# ----------------------------------
# Función principal
# ----------------------------------
def main():
    resultados = asyncio.run(procesar_documentos(contenido))
    guardar_resultado_json(resultados)
    print("✅ Extracción completada. Revisa el archivo 'dataset_extraido.json'.")

if __name__ == "__main__":
    main()

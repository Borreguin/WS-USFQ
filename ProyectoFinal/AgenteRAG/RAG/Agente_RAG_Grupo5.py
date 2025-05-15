import datetime
import csv
import os
import requests
from recuperar_chunks import obtener_chunks_desde_sql

GRUPO = "Grupo 5"
LOG_CSV = "respuestas_grupo5.csv"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "codegemma"

# Inicializar CSV si no existe
with open(LOG_CSV, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(["timestamp", "pregunta", "respuesta"])

def get_completion_sync(prompt: str, model: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model, "messages": [{"role": "user", "content": prompt}]}
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"[ERROR] {e}"

def agente_rag_terminal():
    print(f"🧠 {GRUPO} - Agente RAG en modo terminal")
    print("Escribe 'salir' para terminar el programa.\n")

    while True:
        pregunta = input("❓ Tu pregunta: ").strip()
        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("👋 Cerrando Agente RAG...")
            break

        timestamp = datetime.datetime.now().isoformat(timespec='seconds')
        contexto = obtener_chunks_desde_sql(pregunta)

        if not contexto:
            respuesta = f"{GRUPO} ⚠️ No se encontró información relevante en la base de datos."
        else:
            raw_prompt = f"Usa el siguiente contexto para responder con precisión y claridad:\n\n{contexto}\n\nPregunta: {pregunta}\n\nRespuesta:"
            respuesta_raw = get_completion_sync(raw_prompt, MODEL)
            respuesta = f"{GRUPO} 🤖\n\n{respuesta_raw.strip()}"

        print("\n--- RESPUESTA ---")
        print(respuesta)
        print("------------------\n")

        # Guardar en log
        with open(LOG_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, pregunta, respuesta])

if __name__ == "__main__":
    agente_rag_terminal()

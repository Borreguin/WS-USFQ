import asyncio
from connection.openai_connection import get_completion
from utils.data_loader import contexto_pdf


while True:
    question = input("Pregunta (s para salir): ")
    print("\n")
    if question.lower() == "s":
        break
    # Usar el contexto extraído del PDF
    prompt = f"""
    Eres un asistente de IA que responde preguntas sobre los incidentes reportados dentro de una empresa, segun los documentos registrados.\n
    Tu tarea es responder preguntas de manera precisa y concisa.
    \nSi no sabes la respuesta, di 'No lo sé'.
    
    \n\nPregunta: {question}
    \nContexto: {contexto_pdf}
    \nRespuesta:
    
    """
    completion = asyncio.run(get_completion(prompt))
    print("\n\nRespuesta:", completion, "\n\n")



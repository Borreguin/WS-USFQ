from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate

from utils.data_loader import retriever

model = OllamaLLM(model="llama3.2")

template = """ 

Eres un asistente de IA que responde preguntas sobre los incidentes reportados dentro de una empresa, segun los documentos registrados.
Tu tarea es responder preguntas de manera precisa y concisa. 
Si no sabes la respuesta, di "No lo sé".

Pregunta: {question}
Respuesta: {answer}

"""


prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    question = input("Pregunta (s para salir): ")
    print("\n\n")
    if question.lower() == "s":
        break
    answers = retriever.invoke(question)
    result = chain.invoke({"question": question, "answer": answers})
    print(result)


   
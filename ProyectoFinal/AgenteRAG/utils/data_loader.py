import os
import PyPDF2

pdf_files = [
    os.path.join(os.path.dirname(__file__), '../data/AccionDePersonal.pdf'),
    os.path.join(os.path.dirname(__file__), '../data/DiarioDeGerente.pdf'),
    os.path.join(os.path.dirname(__file__), '../data/EmailPersonal.pdf'),
    os.path.join(os.path.dirname(__file__), '../data/ReporteIncidentes.pdf'),
]

# Extraer texto de los PDFs
def get_pdf_context(pdf_path):
    """Extrae y retorna el texto de un PDF como string."""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
<<<<<<< HEAD
    return pdf_text

# Concatena el texto de todos los PDFs
contexto_pdf = "\n\n".join([get_pdf_context(path) for path in pdf_files])
=======
    # Crear un solo documento con el texto extraído
    document = Document(
        page_content=pdf_text,
        metadata={"source": pdf_path},
        id="0"
    )
    documents.append(document)
    ids.append("0")


vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
>>>>>>> 1f06d75bc3cfb2ab3e6addfe57b1b3394c4c7c5d

